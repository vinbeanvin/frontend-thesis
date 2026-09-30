"""
disease_forecast_routes.py - Disease Forecasting & Analytics Routes
====================================================================
All routes for the Disease Forecasting module.

Access Control:
    /disease/dashboard   - All logged-in users (view)
    /disease/reports     - All logged-in users (view/export)
    /disease/manage      - ADMIN and SUPERADMIN only
    /disease/add-disease - ADMIN and SUPERADMIN only (POST)
    /disease/add-case    - ADMIN and SUPERADMIN only (POST)
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
    Shows: Forecasted Disease Trends, Age-Group Analysis, Forecasted Disease Cases.

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
    Shows forms to add a new disease or record a new case.

    TODO: Pass existing disease list to template for the "Record New Case" dropdown.
    """
    # Future: diseases = Disease.query.all()
    diseases = []  # Placeholder — will come from DB
    return render_template(
        'disease_forecast/manage_records.html',
        active_page='manage',
        diseases=diseases,
    )


# ============================================================
# ADD NEW DISEASE (POST)
# Route: POST /disease/add-disease
# Access: ADMIN, SUPERADMIN only
# ============================================================
@disease_bp.route('/add-disease', methods=['POST'])
@admin_required
def add_disease_record():
    """
    Process the 'Add New Disease' form submission.

    Expects form fields:
        disease_code  - ICD-style code (e.g. ICD-001)
        disease_name  - Full name of the disease
        age_group     - Target age group string
        num_cases     - Initial number of cases (integer)

    TODO: Validate inputs with Flask-WTF, save to Disease table via SQLAlchemy.
    """
    disease_code  = request.form.get('disease_code', '').strip()
    disease_name  = request.form.get('disease_name', '').strip()
    age_group     = request.form.get('age_group', '').strip()
    num_cases     = request.form.get('num_cases', 0)

    # --- Basic validation ---
    if not disease_code or not disease_name:
        flash('Disease Code and Name are required.', 'error')
        return redirect(url_for('disease.manage_records'))

    # TODO: Save to database
    # new_disease = Disease(code=disease_code, name=disease_name, age_group=age_group, cases=num_cases)
    # db.session.add(new_disease)
    # db.session.commit()

    flash(f'Disease "{disease_name}" added successfully.', 'success')
    return redirect(url_for('disease.manage_records'))


# ============================================================
# ADD NEW CASE TO EXISTING DISEASE (POST)
# Route: POST /disease/add-case
# Access: ADMIN, SUPERADMIN only
# ============================================================
@disease_bp.route('/add-case', methods=['POST'])
@admin_required
def add_case_record():
    """
    Process the 'Record New Case' form submission.

    Expects form fields:
        disease_code  - Selected from existing disease list
        disease_name  - Auto-filled (read-only), confirmed here server-side
        age_group     - Age group affected
        num_cases     - Number of new cases to record

    TODO: Look up the disease by code, append a new DiseaseCase record.
    """
    disease_code  = request.form.get('disease_code', '').strip()
    age_group     = request.form.get('age_group', '').strip()
    num_cases     = request.form.get('num_cases', 0)

    if not disease_code:
        flash('Please select a Disease Code.', 'error')
        return redirect(url_for('disease.manage_records'))

    # TODO: Validate disease_code exists, save new case record
    # disease = Disease.query.filter_by(code=disease_code).first_or_404()
    # new_case = DiseaseCase(disease_id=disease.id, age_group=age_group, num_cases=num_cases)
    # db.session.add(new_case)
    # db.session.commit()

    flash(f'Case recorded successfully for disease code "{disease_code}".', 'success')
    return redirect(url_for('disease.manage_records'))
