from flask import Flask
from flask_script import Manager
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
# Database connection
url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)
manager = Manager(app)
@manager.command
def run():
    """Run the Flask application."""
    app.run()
if __name__ == '__main__':
    manager.run()