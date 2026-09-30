"""
main_routes.py - Main Dashboard Routes
=======================================
Handles the main dashboard page and root URL redirect.

Routes:
    GET /           - Redirects to login page
    GET /dashboard  - Main dashboard with module selection cards

This is the central hub after login, allowing users to choose
between Disease Forecast and Medicine Inventory modules.
"""

from flask import Blueprint, render_template, redirect, url_for
from routes.auth_routes import login_required


# ============================================================
# Blueprint Definition
# ============================================================
main_bp = Blueprint('main', __name__)


# ============================================================
# ROOT URL REDIRECT
# Route: /
# Purpose: Redirect to login page when visiting the root URL
# ============================================================
@main_bp.route('/')
def index():
    """Redirect root URL to the login page."""
    return redirect(url_for('auth.login'))


# ============================================================
# MAIN DASHBOARD
# Route: /dashboard
# Purpose: Central hub with Disease Forecast & Medicine Inventory cards
# ============================================================
@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Render the main dashboard page.
    
    Displays two module cards:
    - Disease Forecast (links to /disease/forecast)
    - Medicine Inventory (links to /medicine/management)
    """
    return render_template('main_dashboard.html')
