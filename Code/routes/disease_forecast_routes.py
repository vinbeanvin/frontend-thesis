"""
disease_forecast_routes.py - Disease Forecasting & Analytics Routes
====================================================================
All routes for the Disease Forecasting module.

Access Control:
    /disease/dashboard   - All logged-in users (view)
    /disease/reports     - All logged-in users (view/export)
    /disease/manage      - ADMIN and SUPERADMIN only
    /disease/add-record  - ADMIN and SUPERADMIN only (POST)
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from .auth_routes import login_required, admin_required

disease_bp = Blueprint('disease', __name__, url_prefix='/disease')


# ============================================================
# DASHBOARD
# Route: GET /disease/dashboard
# Access: All logged-in users
# ============================================================
@disease_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Disease Forecasting Dashboard.
    Shows: Forecasted Disease Trends, Forecasted Disease Cases.

    TODO: Pass chart data from ML model to template context.
    """
    return render_template('disease_forecast/dashboard.html', active_page='dashboard')


# ============================================================
# DISEASE REPORTS
# Route: GET /disease/reports
# Access: All logged-in users
# ============================================================
@disease_bp.route('/reports')
@login_required
def reports():
    """
    Disease Reports page.
    Allows user to select a reporting period (monthly) and generate/export a PDF.

    TODO:
        - Read 'period', 'from_month', 'to_month' from request.args
        - Query forecast data from the database for the selected period
        - Pass data to template for display and PDF generation
    """
    # Get selected period from query params (form uses GET)
    period     = request.args.get('period', '')
    from_month = request.args.get('from_month', '')
    to_month   = request.args.get('to_month', '')

    return render_template(
        'disease_forecast/reports.html',
        active_page='reports',
        period=period,
        from_month=from_month,
        to_month=to_month,
    )


# ============================================================
# MANAGE DISEASE RECORDS PAGE
# Route: GET /disease/manage
# Access: ADMIN, SUPERADMIN only
# ============================================================
@disease_bp.route('/manage')
@admin_required
def manage_records():
    """
    Manage Disease Records landing page.
    Shows the combined form to add a new disease or record a new case.

    TODO: Pass existing disease list to template for the DataList dropdown.
    """
    # Future: diseases = Disease.query.all()
    diseases = []  # Placeholder - will come from DB
    return render_template(
        'disease_forecast/manage_records.html',
        active_page='manage',
        diseases=diseases,
    )


# ============================================================
# ADD DISEASE / CASE RECORD (POST)
# Route: POST /disease/add-record
# Access: ADMIN, SUPERADMIN only
# ============================================================
@disease_bp.route('/add-record', methods=['POST'])
@admin_required
def add_record():
    """
    Process the combined 'Add Disease / Record Case' form submission.

    Expects form fields:
        disease_name      - Full name of the disease (Typed or Selected)
        record_month_year - Month and Year for the record (e.g. YYYY-MM)
        age_group[]       - Array of target age group strings
        num_cases[]       - Array of initial number of cases (integers)

    TODO: 
    1. Check if disease_name exists in Disease table. If not, create it.
    2. Save records to DiseaseCase table via SQLAlchemy.
    """
    disease_name      = request.form.get('disease_name', '').strip()
    record_month_year = request.form.get('record_month_year', '').strip()
    age_groups        = request.form.getlist('age_group[]')
    num_cases         = request.form.getlist('num_cases[]')

    # --- Basic validation ---
    if not disease_name:
        flash('Disease Name is required.', 'error')
        return redirect(url_for('disease.manage_records'))
        
    if not record_month_year:
        flash('Month and Year are required.', 'error')
        return redirect(url_for('disease.manage_records'))

    if not age_groups or not num_cases:
        flash('At least one age group and case count is required.', 'error')
        return redirect(url_for('disease.manage_records'))

    # TODO: Save to database
    # disease = Disease.query.filter_by(name=disease_name).first()
    # if not disease:
    #     disease = Disease(name=disease_name)
    #     db.session.add(disease)
    #     db.session.commit()
    # 
    # for age, cases in zip(age_groups, num_cases):
    #     case_record = DiseaseCase(disease_id=disease.id, age_group=age, num_cases=cases, record_date=record_month_year)
    #     db.session.add(case_record)
    # db.session.commit()

    flash(f'Record for "{disease_name}" ({record_month_year}) saved successfully.', 'success')
    return redirect(url_for('disease.manage_records'))
