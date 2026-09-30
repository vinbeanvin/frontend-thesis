"""
auth_routes.py - Authentication & Role-Based Access Control
============================================================
Handles login, logout, and access control decorators.

ROLES:
    SUPERADMIN     - Full access to BOTH Disease Forecasting AND Medicine Inventory
    ADMIN          - Full access to Disease Forecasting; View-only for Medicine
    INVENTORY_STAFF - Full access to Medicine Inventory; View-only for Disease

Hardcoded test accounts (replace with DB later):
    superadmin / super123  -> SUPERADMIN
    admin      / admin123  -> ADMIN
    staff      / staff123  -> INVENTORY_STAFF
"""

from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, session, request

auth_bp = Blueprint('auth', __name__)


# ============================================================
# ROLE CONSTANTS  (use these everywhere, not raw strings)
# ============================================================
ROLE_SUPERADMIN      = 'SUPERADMIN'
ROLE_ADMIN           = 'ADMIN'
ROLE_INVENTORY_STAFF = 'INVENTORY_STAFF'

# Roles that have full Disease Forecasting access
DISEASE_FULL_ACCESS  = {ROLE_SUPERADMIN, ROLE_ADMIN}

# Roles that have full Medicine Inventory access
MEDICINE_FULL_ACCESS = {ROLE_SUPERADMIN, ROLE_INVENTORY_STAFF}

# Roles that can view (but not manage) Disease Forecasting
DISEASE_VIEW_ROLES   = {ROLE_SUPERADMIN, ROLE_ADMIN, ROLE_INVENTORY_STAFF}

# Roles that can view (but not manage) Medicine Inventory
MEDICINE_VIEW_ROLES  = {ROLE_SUPERADMIN, ROLE_ADMIN, ROLE_INVENTORY_STAFF}


# ============================================================
# DECORATORS
# ============================================================

def login_required(f):
    """
    Protect any route that needs an authenticated user.
    Redirects to login page if not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Protect routes that require Disease Forecasting FULL access.
    Allowed roles: SUPERADMIN, ADMIN
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        if session.get('role') not in DISEASE_FULL_ACCESS:
            flash('Access Denied. Administrator privileges required.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def staff_required(f):
    """
    Protect routes that require Medicine Inventory FULL access.
    Allowed roles: SUPERADMIN, INVENTORY_STAFF
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        if session.get('role') not in MEDICINE_FULL_ACCESS:
            flash('Access Denied. Inventory Staff privileges required.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================
# LOGIN PAGE
# Route: GET /login  -> Show form
# Route: POST /login -> Authenticate user
# ============================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle login form display and credential verification.

    TODO: Replace hardcoded accounts with database lookup.
          Use werkzeug.security.check_password_hash() for passwords.
    """
    # Redirect already-logged-in users straight to dashboard
    if session.get('logged_in'):
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # --- HARDCODED ACCOUNTS (replace with DB lookup) ---
        accounts = {
            'superadmin': {
                'password': 'super123',
                'display_name': 'Super Administrator',
                'role': ROLE_SUPERADMIN,
            },
            'admin': {
                'password': 'admin123',
                'display_name': 'Administrator',
                'role': ROLE_ADMIN,
            },
            'staff': {
                'password': 'staff123',
                'display_name': 'Inventory Staff',
                'role': ROLE_INVENTORY_STAFF,
            },
        }

        user = accounts.get(username)
        if user and user['password'] == password:
            # Successful login — store user info in session
            session['logged_in']   = True
            session['username']    = user['display_name']
            session['role']        = user['role']
            flash(f"Welcome back, {user['display_name']}!", 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


# ============================================================
# LOGOUT
# Route: GET /logout
# ============================================================
@auth_bp.route('/logout')
def logout():
    """Clear the session and redirect to login."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
