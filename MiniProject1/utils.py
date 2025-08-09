from datetime import datetime

def initialize_session_state():
    """Initialize session state variables"""
    import streamlit as st
    if 'appointments' not in st.session_state:
        st.session_state.appointments = []

def process_appointments():
    """Process the appointments in session state"""
    import streamlit as st
    if 'appointments' in st.session_state:
        # Add any processing logic here
        pass

def add_manual_appointment(person_name, appointment_type, appointment_date, appointment_time):
    """Add a manual appointment to the session state"""
    import streamlit as st
    if 'appointments' in st.session_state:
        appointment = {
            'person_name': person_name,
            'type': appointment_type,
            'date': appointment_date.strftime("%Y-%m-%d"),
            'time': appointment_time.strftime("%H:%M"),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.appointments.append(appointment) 