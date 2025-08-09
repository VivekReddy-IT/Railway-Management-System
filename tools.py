from logger import setup_logger
from datetime import datetime, timedelta
# import streamlit as st # Remove streamlit import if not used directly in tools (session state moved to database.py)
from database import create_reservation # Import the new function
# Import your Flask models and database session here, e.g.:
# from app import db, Train, Reservation, Station

logger = setup_logger(__name__)

# Remove the old book_appointment function that used session state
# def book_appointment(train_id: str, journey_date: str, source: str, destination: str, passengers: list) -> str:
#     """Books a train ticket for the user."""
#     logger.info(f"Tool: book_appointment called with train_id={train_id}, journey_date={journey_date}, source={source}, destination={destination}, passengers={passengers}")
    
#     try:
#         # Create a new appointment in session state
#         appointment = {
#             'train_id': train_id,
#             'journey_date': journey_date,
#             'source': source,
#             'destination': destination,
#             'passengers': passengers,
#             'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
        
#         if 'appointments' not in st.session_state:
#             st.session_state.appointments = []
            
#         st.session_state.appointments.append(appointment)
#         return f"Successfully booked train {train_id} from {source} to {destination} on {journey_date}"
#     except Exception as e:
#         logger.error(f"Error booking ticket: {e}")
#         return f"Failed to book ticket: {str(e)}"

def get_next_available_appointment(train_id: str, date: str) -> str:
    """Finds the next available booking details for a specific train and date."""
    logger.info(f"Tool: get_next_available_appointment called with train_id={train_id}, date={date}")
    
    try:
        # Simple implementation - returns next day at 9 AM
        next_day = datetime.now() + timedelta(days=1)
        return f"Next available slot for train {train_id}: {next_day.strftime('%Y-%m-%d')} at 09:00"
    except Exception as e:
        logger.error(f"Error getting availability: {e}")
        return f"Failed to get availability: {str(e)}"

def cancel_appointment(pnr: str) -> str:
    """Cancels a train reservation using the PNR."""
    logger.info(f"Tool: cancel_appointment called with pnr={pnr}")
    
    try:
        # This still uses session state - need to update to database interaction
        if 'appointments' not in st.session_state:
            return "No appointments found"
            
        # Find and remove the appointment
        for i, appointment in enumerate(st.session_state.appointments):
            if appointment.get('pnr') == pnr:
                st.session_state.appointments.pop(i)
                return f"Successfully cancelled reservation with PNR: {pnr}"
                
        return f"No reservation found with PNR: {pnr}"
    except Exception as e:
        logger.error(f"Error cancelling reservation: {e}")
        return f"Failed to cancel reservation: {str(e)}"

# Define the book_appointment function to call the database function
def book_appointment(train_id: str, journey_date: str, source: str, destination: str, passengers: list) -> dict:
    """Books a train ticket for the user by calling the database function."""
    logger.info(f"Tool: book_appointment called with train_id={train_id}, journey_date={journey_date}, source={source}, destination={destination}, passengers={passengers}")
    
    # Call the database function to create the reservation
    booking_result = create_reservation(train_id, journey_date, source, destination, passengers)
    
    if booking_result.get("success"):
        # Return the detailed booking information
        return booking_result
    else:
        # Return the error information
        return booking_result

def get_next_available_appointment(train_id: str, date: str) -> str:
    """Finds the next available booking details for a specific train and date, including seat availability and fare."""
    logger.info(f"Tool: get_next_available_appointment called with train_id={train_id}, date={date}")
    # TODO: Implement actual logic to query seat availability and fare based on train_id and date.
    # This should interact with your database to check available seats for AC and Non-AC coaches.
    
    # Placeholder implementation:
    # try:
    #     train = Train.query.get(train_id)
    #     if not train:
    #         return "Train not found."
    #     # Example: Query for available seats for the given date
    #     # available_ac = check_available_seats(train_id, date, 'AC')
    #     # available_nonac = check_available_seats(train_id, date, 'NONAC')
    #     # fare = train.base_fare # Or calculated based on date/quota
    #     
    #     # return f"Available seats for Train {train.name} on {date}: AC: {available_ac}, Non-AC: {available_nonac}. Base Fare: {fare}"
    # except Exception as e:
    #     logger.error(f"Error getting availability: {e}")
    #     return f"Failed to get availability: {e}"

    # Returning dummy availability for now
    return f"Availability check for Train {train_id} on {date}. This is a placeholder response. AC Available: 50, Non-AC Available: 100. Please implement the actual availability logic in tools.py."

def cancel_appointment(pnr: str) -> str:
    """Cancels a train reservation using the PNR."""
    logger.info(f"Tool: cancel_appointment called with pnr={pnr}")
    # TODO: Implement actual cancellation logic here.
    # This should interact with your database to find and update the reservation status.

    # Placeholder implementation:
    # try:
    #     reservation = Reservation.query.filter_by(pnr=pnr).first()
    #     if not reservation:
    #         return "Reservation not found."
    #     # Example: Update the status of the reservation
    #     # reservation.status = 'CANCELLED'
    #     # db.session.commit()
    #     # return f"Reservation {pnr} cancelled successfully."
    # except Exception as e:
    #     db.session.rollback() # Rollback in case of error
    #     logger.error(f"Error cancelling reservation: {e}")
    #     return f"Failed to cancel reservation: {e}"
    
    # Returning a dummy cancellation message for now
    return f"Cancellation request received for PNR {pnr}. This is a placeholder response. Please implement the actual cancellation logic in tools.py." 