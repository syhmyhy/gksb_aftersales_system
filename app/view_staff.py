# app\view_staff.py

from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
from app.controllers import staff_controller
from app.models.staff_model import Staff
from app import app, db
from werkzeug.security import check_password_hash, generate_password_hash # Import the generate_password_hash function

def prevent_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'no-store'
    return response

# Staff Routes
@app.route('/register_staff', methods=['GET', 'POST'])
def register_staff():
    return staff_controller.process_staff_registration()

@app.route('/show_staff_registration_form')
def show_staff_registration_form():
    return staff_controller.show_staff_registration_form()

@app.route('/registration_status')
def registration_status():
    return staff_controller.registration_status()

@app.route('/approve_staff/<staff_id>', methods=['POST'])
def approve_staff(staff_id):
    return staff_controller.approve_staff(staff_id)

@app.route('/reject_staff/<staff_id>', methods=['POST'])
def reject_staff(staff_id):
    return staff_controller.reject_staff(staff_id)

@app.route('/show_staff_profile')
def show_staff_profile():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses halaman ini', 'error')
        return redirect(url_for('show_login_form'))

    staff_id = session['staff_id']
    staff = Staff.query.filter_by(staffID=staff_id).first()

    if not staff:
        flash('Rekod Staff tidak dijumpai', 'error')
        return redirect(url_for('select_page'))  # Redirect to home page if staff record not found

    return render_template('staff_profile.html', staff=staff)

@app.route('/update_staff_profile', methods=['POST'])
def update_staff_profile():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')  
        return redirect(url_for('show_login_form'))

    staff_id = session['staff_id']
    staff = Staff.query.filter_by(staffID=staff_id).first()

    if not staff:
        flash('Rekod Staff tidak dijumpai', 'error')
        return redirect(url_for('select_page'))

    try:
        # Update staff profile with form data
        staff.staffEmail = request.form['staffEmail']
        staff.staffName = request.form['staffName']
        staff.department = request.form['department']
        staff.role = request.form['role']

        # Check if the user wants to change the password
        if 'currentPassword' in request.form and 'newPassword' in request.form and 'confirmPassword' in request.form:
            current_password = request.form['currentPassword']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']

            # Check if new password fields are provided and match
            if new_password and confirm_password and new_password == confirm_password:
                # Check if the current password is correct
                if not check_password_hash(staff.password, current_password):
                    flash('Kata Laluan Semasa tidak sah', 'error')
                    return redirect(url_for('show_staff_profile'))

                # Hash the new password before updating
                hashed_password = generate_password_hash(new_password)
                staff.password = hashed_password

        # Commit changes to the database
        db.session.commit()
        flash('Profil Staff berjaya dikemaskini', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal mengemaskini profil Staff: {str(e)}', 'error')

    return redirect(url_for('select_page'))
