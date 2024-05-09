# app\controllers\staff_controller.py

from flask import render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Staff
from werkzeug.security import generate_password_hash

def process_staff_registration():
    if request.method == 'POST':
        staff_id = request.form['staffID']
        staff_email = request.form['staffEmail']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        password = request.form['password']
        role = request.form['role']

        # Check if staff ID already exists
        existing_staff = Staff.query.filter_by(staffID=staff_id).first()
        if existing_staff:
            flash('Staff ID telah wujud. Sila cuba lagi', 'error')
            return redirect(url_for('show_staff_registration_form'))

        # Hash the password before storing in the database
        hashed_password = generate_password_hash(password)

        # Create a new staff member record
        new_staff = Staff(staffID=staff_id, staffEmail=staff_email, firstName=first_name, lastName=last_name, password=hashed_password, role=role)

        try:
            db.session.add(new_staff)
            db.session.commit()
            flash('Pendaftaran staff telah berjaya. Sila log masuk.', 'success')
            return redirect(url_for('show_login_form'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal mendaftarkan Staff: {str(e)}', 'error')

    # Redirect to staff registration form if not a POST request or if registration fails
    return redirect(url_for('show_staff_registration_form'))

def show_staff_registration_form():
    return render_template('registerstaff.html')