import os
from dotenv import load_dotenv
import sys

# Get the absolute path to the .env file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

# Load environment variables
try:
    if not os.path.exists(env_path):
        print(f"Error: .env file not found at {env_path}")
        sys.exit(1)
    
    load_dotenv(dotenv_path=env_path, encoding='utf-8')
    print(f"Loaded .env file from {env_path}")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY not found in environment variables")
    print("Please make sure your .env file contains the GROQ_API_KEY")
    sys.exit(1)

print(f"Successfully loaded GROQ_API_KEY: {GROQ_API_KEY[:10]}...")

# Model Settings
DEFAULT_MODEL = "mixtral-8x7b-32768"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1024

# Application Settings
APP_NAME = "Rail Transit - AI Booking Assistant"
APP_DESCRIPTION = "An AI-powered assistant for train booking and information"

# Time Settings
DEFAULT_TIMEZONE = "UTC"

# Logging Settings
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 