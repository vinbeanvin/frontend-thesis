"""
app.py - MedCheck Application Entry Point
==========================================
Main entry point for the MedCheck web application.
Uses the Application Factory pattern for clean initialization.

To run the application:
    python app.py

The app will be available at http://127.0.0.1:5000
"""

from flask import Flask
from config import Config
from routes import register_blueprints


def create_app():
    """
    Application Factory: Creates and configures the Flask app.
    
    This pattern makes it easy to:
    - Create multiple app instances (for testing)
    - Initialize extensions (database, etc.) cleanly
    - Register blueprints in a centralized way
    
    Returns:
        Flask: The configured Flask application instance.
    """
    # --- Initialize Flask App ---
    app = Flask(__name__)
    
    # --- Load Configuration ---
    app.config.from_object(Config)
    
    # --- Register All Route Blueprints ---
    # Each blueprint is a separate .py file in the routes/ folder
    register_blueprints(app)
    
    # --- Future: Initialize Extensions ---
    # db.init_app(app)          # SQLAlchemy database
    # migrate.init_app(app)     # Flask-Migrate for DB migrations
    # login_manager.init_app(app)  # Flask-Login for session management
    
    return app


# ============================================================
# Run the Application
# ============================================================
if __name__ == '__main__':
    app = create_app()
    
    # Debug=True enables auto-reload and detailed error pages
    # Change host to '0.0.0.0' to allow external access
    app.run(debug=True, host='127.0.0.1', port=5000)
