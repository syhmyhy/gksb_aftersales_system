# app\controllers\staff_controller.py

from flask import render_template, request, redirect, url_for, flash, session
from app import db
from app.models.staff_model import Staff
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

def process_staff_registration():
    if request.method == 'POST':
        staff_id = request.form['staffID']
        staff_email = request.form['staffEmail']
        staff_name = request.form['staffName']
        department = request.form['department']
        password = request.form['password']
        role = request.form['role']

        # Hash the password before storing in the database
        hashed_password = generate_password_hash(password)

        # Create a new staff member record (not yet approved)
        new_staff = Staff(staffID=staff_id, staffEmail=staff_email, staffName=staff_name, 
                         department=department, password=hashed_password, role=role, approved=False)

        try:
            db.session.add(new_staff)
            db.session.commit()
            flash('Permohonan pendaftaran staff berjaya. Sila tunggu kelulusan admin.', 'success')
            return redirect(url_for('show_login_form'))
        except IntegrityError:
            db.session.rollback()
            flash('Gagal mendaftarkan Staff: Staff ID atau Email telah wujud.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Gagal mendaftarkan Staff kerana ralat yang tidak diketahui. Sila cuba lagi.', 'error')

    return redirect(url_for('show_staff_registration_form'))

def show_staff_registration_form():
    return render_template('registerstaff.html')

def approve_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if staff:
        staff.approved = True
        db.session.commit()
        flash(f'Staff dengan ID {staff_id} telah diluluskan.', 'success')
    else:
        flash(f'Staff dengan ID {staff_id} tidak dijumpai.', 'error')
    return redirect(url_for('registration_status'))

def reject_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        flash(f'Staff dengan ID {staff_id} telah ditolak dan dipadam.', 'success')
    else:
        flash(f'Staff dengan ID {staff_id} tidak dijumpai.', 'error')
    return redirect(url_for('registration_status'))

def registration_status():
    pending_staff = Staff.query.filter_by(approved=False).all()
    return render_template('registration_status.html', pending_staff=pending_staff)