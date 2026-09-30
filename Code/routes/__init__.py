"""
routes/__init__.py - Blueprint Registration
============================================
Registers all route blueprints with the Flask application.
Each blueprint corresponds to a separate .py file for easy debugging.

Blueprints:
    - auth_bp   : Login/Logout routes         (auth_routes.py)
    - main_bp   : Main dashboard              (main_routes.py)
    - disease_bp: Disease Forecast module      (disease_forecast_routes.py)
    - medicine_bp: Medicine Inventory module   (medicine_inventory_routes.py)
"""

from routes.auth_routes import auth_bp
from routes.main_routes import main_bp
from routes.disease_forecast_routes import disease_bp
from routes.medicine_inventory_routes import medicine_bp


def register_blueprints(app):
    """
    Register all blueprints with the Flask app.
    
    Args:
        app: The Flask application instance.
    """
    app.register_blueprint(auth_bp)       # Login/Logout
    app.register_blueprint(main_bp)       # Main Dashboard
    app.register_blueprint(disease_bp)    # Disease Forecast module
    app.register_blueprint(medicine_bp)   # Medicine Inventory module
