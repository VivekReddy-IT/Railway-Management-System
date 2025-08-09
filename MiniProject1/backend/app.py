from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_mail import Mail

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/railway_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['MAIL_USERNAME'] = 'gajulavivekananda3@gmail.com'  # (replace with your Gmail address)
app.config['MAIL_PASSWORD'] = 'qdpnobafnribkzax'      # (no spaces, just the 16 characters)
app.config['MAIL_DEFAULT_SENDER'] = 'gajulavivekananda3@gmail.com'

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
mail = Mail(app)

# Import models and routes
from models import *
from routes import *

@app.route('/')
def index():
    return 'Welcome to the Railway Reservation System API!'

if __name__ == '__main__':
    app.run(debug=True) 