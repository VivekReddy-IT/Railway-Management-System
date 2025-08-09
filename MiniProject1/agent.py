from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from typing import List, Dict, Any, TypedDict
import os
import sys
import json
import re # Import regex for parsing tool calls
# Assuming config, constants, logger, and tools modules exist and are correctly configured
from config import AppConfig
from constants import GROQ_API_KEY
from logger import setup_logger
from tools import book_appointment, get_next_available_appointment, cancel_appointment
from database import get_all_trains, search_stations, get_train_route # Import new database tools
from ticket_generator import generate_ticket_pdf # Import the PDF generation function

logger = setup_logger(__name__)

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logger.error("GROQ_API_KEY environment variable is not set. Please set it in your .env file.")
    print("Error: GROQ_API_KEY environment variable is not set. Please set it in your .env file.")
    print("1. Create a .env file in your project root directory")
    print("2. Add this line to it: GROQ_API_KEY=your-actual-groq-api-key-here")
    print("3. Replace 'your-actual-groq-api-key-here' with your actual GROQ API key from https://console.groq.com/")
    sys.exit(1)

try:
    config = AppConfig()
    # Initialize LLM with the API key from environment variable
    llm = ChatGroq(model=config.model_name, api_key=api_key)
    logger.info(f"LLM initialized with model: {llm}")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {str(e)}")
    print(f"Error: Failed to initialize LLM: {str(e)}")
    print("Please make sure you have a valid GROQ API key and internet connection.")
    sys.exit(1)

class AgentState(TypedDict):
    messages: List[Any]
    current_time: str

# Removed global CONVERSATION, will manage via session in Flask app

def receive_message_from_caller(message: str, conversation_history: List[Any], current_time: str) -> Dict[str, Any]:
    """
    Process a message from the caller and return the updated conversation history.
    This function works with Streamlit's session state by accepting and returning the conversation history.
    
    Args:
        message (str): The user's message
        conversation_history (List[Any]): The current conversation history from Streamlit's session state
        current_time (str): The current time string
    
    Returns:
        Dict[str, Any]: A dictionary containing the updated conversation history
    """
    logger.info(f"Agent received message: {message}")
    logger.debug(f"Conversation history received: {conversation_history}")
    logger.debug(f"Current time received: {current_time}")
    # Use the conversation history passed in
    current_conversation = conversation_history + [HumanMessage(content=message)]
    state: AgentState = {
        "messages": current_conversation,
        "current_time": current_time
    }
    logger.debug(f"State before invoke: {state}")
    try:
        # Pass the state to the compiled graph
        new_state = caller_app.invoke(state)
        logger.debug(f"New state after invoke: {new_state}")
        # Return the updated conversation
        return {
            "messages": new_state["messages"]
        }
    except Exception as e:
        logger.exception(f"Error in receive_message_from_caller: {str(e)}")
        # Return error message and current conversation history
        return {
            "messages": current_conversation + [AIMessage(content="I'm sorry, I encountered an error processing your request.")],
        }

def should_continue_caller(state: AgentState) -> str:
    logger.debug(f"Entering should_continue_caller with state: {state}")
    messages = state["messages"]
    if not messages:
        logger.warning("No messages in state")
        return "end"
    last_message = messages[-1]
    # Check if the last message is an AIMessage and has content (not just tool calls)
    if isinstance(last_message, AIMessage) and last_message.content and "<tool_call>" not in last_message.content:
        logger.info("Ending conversation")
        return "end"
    else:
        logger.info("Continuing conversation")
        return "continue"

def call_caller_model(state: AgentState) -> AgentState:
    logger.debug(f"Entering call_caller_model with state: {state}")
    messages = state["messages"]
    current_time = state["current_time"]

    try:
        # Ensure the system message is always the first message in the formatted list
        system_message_content = config.CALLER_PA_PROMPT.format(current_time=current_time)
        formatted_messages = [
            SystemMessage(content=system_message_content)
        ]

        # Append all messages from the state, excluding any existing SystemMessages from history
        for m in messages:
            if isinstance(m, (HumanMessage, AIMessage)):
                 # Avoid adding duplicate system messages if they somehow ended up in history
                if not (isinstance(m, SystemMessage) and m.content == system_message_content):
                    formatted_messages.append(m)
            else:
                logger.warning(f"Unexpected message type in history: {type(m)}")

        logger.debug(f"Formatted messages for LLM: {formatted_messages}")

        llm_response = llm.invoke(formatted_messages)
        logger.info(f"LLM response: {llm_response}")

        # Append the LLM's response to the messages
        new_messages = messages + [llm_response]

        new_state = {"messages": new_messages, "current_time": current_time}
        logger.debug(f"New state after LLM response: {new_state}")
        return new_state

    except Exception as e:
        logger.exception(f"Error in call_caller_model: {str(e)}")
        # Append the error message to the messages
        error_message = AIMessage(content="I'm sorry, I encountered an error while processing with the AI. Could you please try again?")
        return {"messages": messages + [error_message],
                "current_time": current_time}

def preprocess_llm_output(state: AgentState) -> AgentState:
    logger.debug(f"Entering preprocess_llm_output with state: {state}")
    last_message = state["messages"][-1]
    # Check if the last message is an AIMessage and contains a tool call marker
    if isinstance(last_message, AIMessage) and last_message.content and "<tool_call>" in last_message.content:
        content = last_message.content
        logger.debug(f"Preprocessing message with tool call: {content}")
        try:
            # Extract the tool call string between the markers
            tool_call_match = re.search(r"<tool_call>(.*?)</tool_call>", content)
            if tool_call_match:
                tool_call_str = tool_call_match.group(1).strip()
                logger.info(f"Extracted tool call string: {tool_call_str}")
                
                # Parse function name and arguments safely
                match = re.match(r"(\w+)\((.*)\)", tool_call_str)
                if match:
                    function_name = match.group(1)
                    args_str = match.group(2)
                    
                    # Safely evaluate arguments (assuming simple key=value or just values)
                    # A more robust approach might use a proper parser or Pydantic
                    args = {}
                    if args_str:
                        try:
                            # Attempt to parse arguments as a JSON object if it looks like one
                            if args_str.startswith('{') and args_str.endswith('}'):
                                args = json.loads(args_str.replace('\'', '"')) # Replace single quotes with double for JSON
                            else:
                                # Otherwise, parse simple key=value pairs or single value
                                for arg in args_str.split(','):
                                    key_value = arg.split('=', 1)
                                    if len(key_value) == 2:
                                        key = key_value[0].strip()
                                        value = key_value[1].strip().strip('\'').strip('"') # Remove quotes
                                        args[key] = value
                                    else:
                                        # Handle cases with a single un-named argument
                                        args['query'] = arg.strip().strip('\'').strip('"')

                        except json.JSONDecodeError:
                             # Fallback if JSON parsing fails
                            logger.warning(f"Could not parse arguments as JSON, attempting key=value parsing: {args_str}")
                            args = {}
                            for arg in args_str.split(','):
                                key_value = arg.split('=', 1)
                                if len(key_value) == 2:
                                    key = key_value[0].strip()
                                    value = key_value[1].strip().strip('\'').strip('"') # Remove quotes
                                    args[key] = value
                                else:
                                     # Handle cases with a single un-named argument
                                     args['query'] = arg.strip().strip('\'').strip('"')
                        except Exception as arg_e:
                            logger.error(f"Unexpected error parsing arguments '{args_str}': {arg_e}")
                            args = {}

                    logger.info(f"Parsed function name: {function_name}, arguments: {args}")
                    
                    # Map function name to the actual Python function
                    available_functions = {
                        "book_appointment": book_appointment,
                        "get_next_available_appointment": get_next_available_appointment,
                        "cancel_appointment": cancel_appointment,
                        "get_all_trains": get_all_trains,
                        "search_stations": search_stations, # Add new tool mapping
                        "get_train_route": get_train_route  # Add new tool mapping
                    }
                    
                    if function_name in available_functions:
                        func_to_call = available_functions[function_name]
                        logger.info(f"Calling function: {function_name} with args: {args}")
                        # Call the function with parsed arguments
                        try:
                            result = func_to_call(**args)
                            logger.info(f"Tool execution successful. Result: {result}")

                            # Check if the successful tool call was book_appointment
                            if function_name == "book_appointment":
                                logger.info(f"book_appointment tool called. Result: {result}")
                                if result.get("success"):
                                    booking_details = result.get("booking_details")
                                    if booking_details:
                                        logger.info(f"Booking successful. Details received: {booking_details}")
                                        # Define output directory and create if it doesn't exist
                                        output_dir = "tickets"
                                        os.makedirs(output_dir, exist_ok=True)
                                        
                                        # Define output path for the PDF
                                        pnr = booking_details.get('pnr', 'ticket')
                                        output_file = os.path.join(output_dir, f"ticket_{pnr}.pdf")
                                        
                                        logger.info(f"Attempting to generate PDF ticket at: {output_file}")
                                        # Generate the PDF ticket
                                        pdf_result = generate_ticket_pdf(booking_details, output_file)
                                        logger.info(f"PDF generation result: {pdf_result}")
                                        
                                        if pdf_result.get("success"):
                                            ticket_message = f"\nYour ticket has been generated (PNR: {pnr}). You can find it at: {output_file}" # Inform user about the ticket
                                            logger.info(f"Ticket generated successfully: {output_file}")
                                        else:
                                            ticket_message = f"\nBooking successful (PNR: {pnr}), but failed to generate ticket: {pdf_result.get('error')}"
                                            logger.error(f"Failed to generate ticket for PNR {pnr}: {pdf_result.get('error')}")
                                        
                                        # Update the AI's message to include booking confirmation and ticket info
                                        confirmation_message = f"Successfully booked train {booking_details.get('train_name', 'N/A')} from {booking_details.get('source_station_name', 'N/A')} to {booking_details.get('destination_station_name', 'N/A')} on {booking_details.get('journey_date', 'N/A')}. PNR: {pnr}."
                                        state["messages"][-1] = AIMessage(content=confirmation_message + ticket_message)
                                    else:
                                         logger.error("book_appointment returned success but no booking_details.")
                                         state["messages"][-1] = AIMessage(content="Booking successful, but could not retrieve booking details.")
                                else:
                                    # Handle booking failure
                                    error_message = result.get("error", "Unknown booking error.")
                                    logger.error(f"book_appointment failed. Error: {error_message}")
                                    state["messages"][-1] = AIMessage(content=f"Booking failed: {error_message}")
                            elif function_name == "book_appointment" and result.get("success") is False:
                                # Handle booking failure
                                error_message = result.get("error", "Unknown booking error.")
                                state["messages"][-1] = AIMessage(content=f"Booking failed: {error_message}")
                            else:
                                # For other tools, just return the result
                                state["messages"][-1] = AIMessage(content=f"Tool Result: {result}")

                        except TypeError as type_e:
                            logger.error(f"TypeError when calling {function_name} with args {args}: {type_e}")
                            state["messages"][-1] = AIMessage(content=f"Error calling tool {function_name}: Invalid arguments provided. {type_e}")
                        except Exception as exec_e:
                             logger.exception(f"Error during execution of tool {function_name} with args {args}: {exec_e}")
                             state["messages"][-1] = AIMessage(content=f"Error executing tool {function_name}: {exec_e}")
                    else:
                        logger.warning(f"Tool function not found: {function_name}")
                        state["messages"][-1] = AIMessage(content=f"Tool function not found: {function_name}")
                else:
                    logger.warning(f"Could not parse tool call string format: {tool_call_str}")
                    state["messages"][-1] = AIMessage(content=f"Invalid tool call format: {tool_call_str}")
            else:
                logger.warning("Tool call marker found but content could not be extracted.")
                state["messages"][-1] = AIMessage(content="Error processing tool call.")

        except Exception as e:
            logger.exception(f"Unexpected error in preprocess_llm_output: {str(e)}")
            # If any other error occurs during preprocessing/execution
            state["messages"][-1] = AIMessage(content=f"An unexpected error occurred during tool processing: {str(e)}")

    # If the last message is not an AIMessage or doesn't contain a tool call marker,
    # pass it through unchanged. This handles cases where the LLM directly responds.
    else:
         logger.debug("Last message does not contain a tool call marker, passing through.")
         # No change needed to state
         pass

    logger.debug(f"State after preprocess: {state}")
    return state

# Define the tools accessible to the agent
# Ensure these functions exist in your tools.py file
caller_tools_list = [
    book_appointment,
    get_next_available_appointment,
    cancel_appointment,
    get_all_trains,       # Existing database tool
    search_stations,      # New database tool
    get_train_route       # New database tool
]
# Create a ToolNode from the list of tools
tool_node = ToolNode(caller_tools_list)
logger.info(f"Tools initialized for ToolNode: {caller_tools_list}")

# Define the workflow using LangGraph
caller_workflow = StateGraph(AgentState)

# Add Nodes: agent (calls LLM), preprocess (handles tool calls), action (executes tools)
caller_workflow.add_node("agent", call_caller_model)
caller_workflow.add_node("preprocess", preprocess_llm_output)
caller_workflow.add_node("action", tool_node)

# Add Edges:
# From 'agent', decide whether to preprocess (if likely a tool call) or end (if final response)
# NOTE: The should_continue_caller logic needs to be refined to detect tool calls more reliably
# A common pattern is for the LLM to format tool calls in a specific way that can be parsed.
# The current preprocess_llm_output looks for '<tool_call>', so should_continue_caller should check for this.
caller_workflow.add_conditional_edges(
    "agent",
    should_continue_caller, # This function determines the next step based on agent output
    {
        # If should_continue_caller returns "continue", go to preprocess (assuming it means processing required)
        # You might adjust the logic here based on how your LLM indicates tool use vs final answer
        "continue": "preprocess", 
        "end": END, # If should_continue_caller returns "end", the workflow finishes
    },
)

# After preprocessing, always go to action (execute the tool)
caller_workflow.add_edge("preprocess", "action")

# After action (tool execution), always go back to the agent to interpret the tool result and continue the conversation
caller_workflow.add_edge("action", "agent")

# Set the entry point for the workflow
caller_workflow.set_entry_point("agent")

# Compile the graph
caller_app = caller_workflow.compile()
logger.info("Caller workflow compiled successfully")

# --- Helper function to clear conversation history (useful for testing) ---
def clear_conversation(session):
    if 'conversation' in session:
        del session['conversation']
        logger.info("Conversation history cleared from session.")

# --- Helper function to get conversation history from session ---
def get_conversation_history(session):
    if 'conversation' not in session:
        session['conversation'] = []
    return session['conversation']

# --- Helper function to update conversation history in session ---
def update_conversation_history(session, conversation):
    session['conversation'] = conversation
    session.modified = True # Ensure session is marked as modified