# app\controllers\auth_controller.py

from flask import render_template, request, redirect, url_for, flash, session
from app import db
from app.models.staff_model import Staff
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import string

def show_login_form():
    return render_template('login.html')

def login():
    if 'staff_id' in session:
        # If user already has an active session, redirect to home page
        return redirect(url_for('select_page'))

    if request.method == 'POST':
        staff_id = request.form['staffID']
        password = request.form['password']

        staff = Staff.query.filter_by(staffID=staff_id).first()

        if staff and check_password_hash(staff.password, password):
            session['staff_id'] = staff.staffID
            session['staffName'] = staff.staffName
            session['department'] = staff.department
            session['role'] = staff.role  # Set the user's role in the session
            return redirect(url_for('select_page'))
        else:
            flash('Staff ID atau kata laluan tidak sah', 'error')
    
    # If login fails or it's a GET request, show the login form
    return redirect(url_for('show_login_form'))

def logout():
    session.clear()
    flash('Anda berjaya log keluar', 'success')
    return redirect(url_for('show_login_form'))
