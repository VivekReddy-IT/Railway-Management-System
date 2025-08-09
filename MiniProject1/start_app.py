import subprocess
import sys
import os

def main():
    print("Starting Streamlit App...")
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to streamlit_app.py
        app_path = os.path.join(current_dir, "streamlit_app.py")
        # Run the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    except Exception as e:
        print(f"Error: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 