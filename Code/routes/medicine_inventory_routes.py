"""
medicine_inventory_routes.py - Medicine Inventory Routes
=========================================================
All routes for the Medicine Inventory module.

Access Control:
    /medicine/list        - All logged-in users (view)
    /medicine/manage      - INVENTORY_STAFF, SUPERADMIN only
    /medicine/add-medicine- INVENTORY_STAFF, SUPERADMIN only (POST)
    /medicine/camera      - INVENTORY_STAFF, SUPERADMIN only
    /medicine/reports     - All logged-in users (view/export)
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from .auth_routes import login_required, staff_required

medicine_bp = Blueprint('medicine', __name__, url_prefix='/medicine')


# ============================================================
# MEDICINE LIST
# Route: GET /medicine/list
# Access: All logged-in users
# ============================================================
@medicine_bp.route('/list')
@login_required
def list_medicines():
    """
    Medicine List with search/filter and inventory table.
    Shows all medicines with Total Stock, Batch No., Expiry, Status.
    """
    search  = request.args.get('search', '').strip()
    batch   = request.args.get('batch', '').strip()
    expiry  = request.args.get('expiry', '').strip()
    status  = request.args.get('status', '').strip()

    medicines = []
    stats = {
        'total': 0,
        'low_stock': 0,
        'near_expiry': 0,
    }

    return render_template(
        'medicine_inventory/list.html',
        active_page='list',
        medicines=medicines,
        stats=stats,
        search=search,
        batch=batch,
        expiry=expiry,
        status=status,
    )


# ============================================================
# MANAGE MEDICINE (Page)
# Route: GET /medicine/manage
# Access: INVENTORY_STAFF, SUPERADMIN only
# ============================================================
@medicine_bp.route('/manage')
@staff_required
def manage():
    """
    Manage Medicine page.
    - Add new medicine form
    - Search & edit existing medicine
    """
    search_term    = request.args.get('search_medicine', '').strip()
    search_results = []

    return render_template(
        'medicine_inventory/manage.html',
        active_page='manage',
        search_term=search_term,
        search_results=search_results,
    )


# ============================================================
# ADD NEW MEDICINE (POST)
# Route: POST /medicine/add-medicine
# Access: INVENTORY_STAFF, SUPERADMIN only
# ============================================================
@medicine_bp.route('/add-medicine', methods=['POST'])
@staff_required
def add_medicine():
    """
    Process the 'Add New Medicine' form.
    """
    medicine_name = request.form.get('medicine_name', '').strip()

    if not medicine_name:
        flash('Medicine Name is required.', 'error')
        return redirect(url_for('medicine.manage'))

    flash(f'Medicine "{medicine_name}" added to the inventory.', 'success')
    return redirect(url_for('medicine.manage'))


# ============================================================
# CAMERA SCANNER
# Route: GET /medicine/camera
# Access: INVENTORY_STAFF, SUPERADMIN only
# ============================================================
@medicine_bp.route('/camera')
@staff_required
def camera():
    """
    Camera/YOLO scanner page.
    """
    return render_template('medicine_inventory/camera.html', active_page='camera')


# ============================================================
# INVENTORY REPORTS
# Route: GET /medicine/reports
# Access: All logged-in users
# ============================================================
@medicine_bp.route('/reports')
@login_required
def reports():
    """
    Inventory Reports.
    """
    period    = request.args.get('period', '')
    from_date = request.args.get('from_date', '')
    to_date   = request.args.get('to_date', '')

    return render_template(
        'medicine_inventory/reports.html',
        active_page='reports',
        period=period,
        from_date=from_date,
        to_date=to_date,
    )
