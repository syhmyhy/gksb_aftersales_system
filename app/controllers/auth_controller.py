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
    if request.method == 'POST':
        staff_id = request.form['staffID']
        password = request.form['password']
        
        # Find the staff by staffID
        staff = Staff.query.filter_by(staffID=staff_id).first()
        
        if not staff:
            flash('ID Staff tidak dijumpai', 'error')
            return redirect(url_for('show_login_form'))

        # Check if the staff is approved
        if not staff.approved:
            flash('Akaun belum diluluskan.', 'error')
            return redirect(url_for('show_login_form'))

        # Check if the password is correct
        if not check_password_hash(staff.password, password):
            flash('Kata laluan tidak sah', 'error')
            return redirect(url_for('show_login_form'))

        # Log in the staff
        session['staff_id'] = staff.staffID
        return redirect(url_for('select_page'))

    return redirect(url_for('show_login_form'))

def logout():
    session.clear()
    flash('Anda berjaya log keluar', 'success')
    return redirect(url_for('show_login_form'))
