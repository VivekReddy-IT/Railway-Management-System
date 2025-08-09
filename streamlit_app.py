import streamlit as st
import os
from dotenv import load_dotenv
from agent import receive_message_from_caller
from langchain_core.messages import HumanMessage, AIMessage
from datetime import datetime
import utils
from logger import setup_logger
import re # Import the regex module

# Set up logger
logger = setup_logger(__name__)

# Load environment variables
load_dotenv()

# Set page config at the very beginning
st.set_page_config(
    page_title="Rail Transit - AI Booking Assistant",
    page_icon="🚂",
    layout="wide"
)

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if 'appointments' not in st.session_state:
    st.session_state.appointments = []

# Add a new session state variable to store the button click
if 'button_input' not in st.session_state:
    st.session_state.button_input = None

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Main app title
st.title("🚂 Rail Transit - AI Booking Assistant")

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

# Main chat interface in the left column
with col1:
    st.subheader("Chat with AI Assistant")
    
    # Display conversation history
    for message in st.session_state.conversation:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                # Check if the message contains a list of train options
                train_options_match = re.search(r"I found a train matching your search:.*?\n(.*?)Please select a train by its Train ID or number", message.content, re.DOTALL)
                
                if train_options_match:
                    st.write(message.content.split("Please select")[0]) # Display the text before the selection instruction
                    options_text = train_options_match.group(1).strip()
                    options_list = options_text.split('\n')
                    
                    # Display options as buttons
                    st.write("Please select a train:")
                    for option_line in options_list:
                        if option_line.strip():
                            # Extract train ID and name
                            match = re.search(r"\d+\. (.*?) - Train ID: (.*)", option_line)
                            if match:
                                train_name = match.group(1).strip()
                                train_id = match.group(2).strip()
                                button_label = f"{train_name} ({train_id})"
                                
                                # Create a button for each option
                                if st.button(button_label, key=train_id):
                                    st.session_state.button_input = train_id # Store the clicked button's value
                                    st.rerun() # Rerun to process the button click
                else:
                    # Check if the message contains a ticket file path
                    ticket_path_match = re.search(r"You can find it at: (.*?\.pdf)", message.content)
                    
                    if ticket_path_match:
                        ticket_file_path = ticket_path_match.group(1).strip()
                        # Display the message content before the file path
                        st.write(message.content.split("You can find it at:")[0])
                        
                        # Check if the file exists before creating a download button
                        if os.path.exists(ticket_file_path):
                            with open(ticket_file_path, "rb") as file:
                                st.download_button(
                                    label="Download Ticket PDF",
                                    data=file,
                                    file_name=os.path.basename(ticket_file_path),
                                    mime="application/pdf"
                                )
                        else:
                            st.write(f"Generated ticket file not found at: {ticket_file_path}")
                            logger.error(f"Generated ticket file not found at: {ticket_file_path}")

                    else:
                        # If not a train options message or ticket message, display as regular text
                        st.write(message.content)
    
    # Chat input
    user_input = st.chat_input("Ask about trains or booking...")
    
    # Check if a button was clicked and use its value as input
    if st.session_state.button_input:
        user_input = st.session_state.button_input
        st.session_state.button_input = None # Clear the button input after using it
    
    if user_input:
        try:
            # Add user message to conversation
            st.session_state.conversation.append(HumanMessage(content=user_input))
            
            # Get AI response
            current_time = get_current_time()
            response = receive_message_from_caller(user_input, st.session_state.conversation, current_time)
            
            if 'messages' in response:
                st.session_state.conversation = response['messages']
            else:
                logger.error("Agent did not return 'messages' key in output")
                st.session_state.conversation.append(
                    AIMessage(content="I'm sorry, I encountered an error. Please try again.")
                )
        except Exception as e:
            logger.exception(f"Error processing chat message: {str(e)}")
            st.error(f"Error: {str(e)}")
            st.session_state.conversation.append(
                AIMessage(content="I'm sorry, I encountered an error. Please try again.")
            )
        
        # Rerun to update the chat
        st.rerun()

# Debug information in the right column
with col2:
    st.write("🙏")
    st.write("welcome to railtransit") 