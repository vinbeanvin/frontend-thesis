"""
config.py - Application Configuration
======================================
Contains configuration settings for the MedCheck application.
Uses OOP pattern with a Config class for clean organization.

Future: Add database URI, ML model paths, etc.
"""

import os


class Config:
    """
    Base configuration class for the MedCheck application.
    
    Attributes:
        SECRET_KEY: Used for session management and CSRF protection.
        DEBUG: Enable/disable debug mode.
    
    Future additions:
        SQLALCHEMY_DATABASE_URI: Database connection string.
        ML_MODEL_PATH: Path to trained ML models.
    """
    
    # Secret key for session management (change this in production!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'medcheck-dev-secret-key-change-in-production'
    
    # Debug mode (set to False in production)
    DEBUG = True
    
    # --- Future Database Configuration ---
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///medcheck.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- Future ML Model Configuration ---
    # ML_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_models')
