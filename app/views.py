#app\views.py

from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash, jsonify, abort
from app.controllers import auth_controller, job_controller, staff_controller, aftersales_controller
from app.models.aftersales_model import Aftersales
from app.models.job_model import Job
from app.models.staff_model import Staff
from app import app, db
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash # Import the generate_password_hash function
import os

def prevent_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'no-store'
    return response

# Authentication Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'staff_id' in session:
        # If user is logged in, redirect to home page
        return redirect(url_for('home'))

    if request.method == 'POST':
        return auth_controller.login()
    else:
        return auth_controller.show_login_form()

@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    flash('Anda telah berjaya log keluar', 'success')
    return redirect(url_for('show_login_form'))

@app.route('/show_login_form')
def show_login_form():
    if 'staff_id' in session:
        return redirect(url_for('home'))  # Redirect to home if already logged in
    return auth_controller.show_login_form()

# Home and Main Pages
@app.route('/home.html')
def home():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))
    
    staffID = session.get('staff_id')
    print("Staff ID:", staffID)
    print("Session Data:", session)
    return render_template('home.html')

# Aftersales Routes
@app.route('/aftersales.html')
def show_aftersales_form():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))
    return render_template('aftersales.html')

@app.route('/show_aftersales_management')
def show_aftersales_management():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    aftersales_data = Aftersales.query.all()
    return render_template('aftersales_management.html', aftersales_data=aftersales_data)

@app.route('/update_aftersales/<string:registrationNo>', methods=['GET', 'POST'])
def update_aftersales_route(registrationNo):
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    aftersales = Aftersales.query.filter_by(registrationNo=registrationNo).first()
    if not aftersales:
        flash('Rekod Aftersales tidak dijumpai', 'error')
        return redirect(url_for('show_aftersales_management'))

    job = Job.query.filter_by(jobNo=aftersales.jobNo).first()

    if request.method == 'POST':
        try:
            # Update Aftersales record with form data
            aftersales.endUser = request.form['endUser']
            aftersales.bodyType = request.form['bodyType']
            aftersales.chassisType = request.form['chassisType']
            aftersales.chassisModel = request.form['chassisModel']
            aftersales.chassisNo = request.form['chassisNo']
            aftersales.engineNo = request.form['engineNo']
            aftersales.dateDelivered = request.form['dateDelivered']
            aftersales.stateLocality = request.form['stateLocality']
            aftersales.detailLocality = request.form['detailLocality']
            aftersales.chassisMileageWarranty = request.form['chassisMileageWarranty']
            aftersales.chassisPeriodWarranty = request.form['chassisPeriodWarranty']
            aftersales.chassisExpired = request.form['chassisExpired']
            aftersales.bodyPeriodWarranty = request.form['bodyPeriodWarranty']
            aftersales.bodyExpired = request.form['bodyExpired']
            aftersales.noService = request.form['noService']
            aftersales.mileageService = request.form['mileageService']
            aftersales.custPhone = request.form['custPhone']
            aftersales.custEmail = request.form['custEmail']
            aftersales.notes = request.form['notes']
            # aftersales.custFile = request.form['custFile']
            # Add other fields here...

            db.session.commit()
            print("Update Aftersales: ", aftersales)
            flash('Rekod Aftersales berjaya dikemaskini', 'success')
        except KeyError as e:
            flash(f'Gagal mengemaskini rekod: Ruang diperlukan "{e.args[0]}" hilang', 'error')
        except ValueError as e:
            flash(f'Gagal mengemaskini rekod: Nilai tidak sah untuk medan - {str(e)}', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Ralat semasa mengemaskini rekod: {str(e)}', 'error')

        return redirect(url_for('show_aftersales_management'))

    # Render the update form with pre-filled data for GET request
    return render_template('update_aftersales.html', aftersales=aftersales, job=job)

@app.route('/delete_aftersales/<string:registrationNo>', methods=['POST'])
def delete_aftersales_route(registrationNo):
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    aftersales = Aftersales.query.filter_by(registrationNo=registrationNo).first()

    if aftersales:
        try:
            job = Job.query.filter_by(jobNo=aftersales.jobNo).first()

            if job:
                # Decrement aftersales_count for the associated Job
                job.aftersales_count -= 1
                db.session.delete(aftersales)
                db.session.commit()
                flash('Rekod Aftersales berjaya dipadam', 'success')
            else:
                flash('Rekod Aftersales tidak dijumpai', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memadam rekod Aftersales: {e}', 'error')
            return redirect(url_for('show_aftersales_management'))
    else:
        flash('Rekod Aftersales tidak dijumpai', 'error')

    return redirect(url_for('show_aftersales_management'))

@app.route('/submit_aftersales_form', methods=['POST'])
def submit_aftersales_form():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))
    return aftersales_controller.submit_aftersales_form()

# Job Routes
@app.route('/job.html')
def show_job_form():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    staffID = session.get('staff_id')    

    if staffID in ('GSK39', 'GSK51'):
        # Allow access for specific staffID values ('GSK39' or 'GSK51')
        response = make_response(render_template('job.html'))
        return prevent_caching(response)
    else:
        # For all other staffID values, render view-only job content
        job_data = Job.query.all()
        return render_template('viewonly_job.html')

@app.route('/submit_job_form', methods=['POST'])
def submit_job_form():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))
    return job_controller.submit_job_form()

@app.route('/show_job_management')
def show_job_management():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    staffID = session.get('staff_id')
    
    if staffID in ('GSK39', 'GSK51'):
        # Allow access for specific staffID values ('GSK39' or 'GSK51')
        job_data = Job.query.all()
        return render_template('job_management.html', job_data=job_data)
    else:
        # For all other staffID values, render view-only job management content
        job_data = Job.query.all()
        return render_template('viewonly_job_management.html', job_data=job_data)

@app.route('/get_job_details', methods=['GET'])
def get_job_details():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))
    job_no = request.args.get('jobNo')
    return job_controller.get_job_details(job_no)

@app.route('/update_job/<int:jobNo>', methods=['GET', 'POST'])
def update_job_route(jobNo):
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    job = Job.query.get(jobNo)

    if not job:
        flash('Rekod Job tidak dijumpai', 'error')
        return redirect(url_for('show_job_form'))

    if request.method == 'POST':
        try:
            new_quantity = int(request.form['quantity'])

            # Get the current count of aftersales records associated with this job
            current_aftersales_count = job.aftersales_count

            if new_quantity < current_aftersales_count:
                flash('Kuantiti baru tidak boleh kurang daripada jumlah rekod Aftersales yang sedia ada', 'error')
                return redirect(url_for('update_job_route', jobNo=jobNo))

            job.title = request.form['title']
            job.custName = request.form['custName']
            job.vehicleType = request.form['vehicleType']
            job.quantity = new_quantity
            job.dateReceived = request.form['dateReceived']
            job.costUnit = request.form['costUnit']
            job.totalCost = request.form['totalCost']
            job.profitUnit = request.form['profitUnit']
            job.totalProfit = request.form['totalProfit']
            job.jobDateDelivered = request.form['jobDateDelivered']

            db.session.commit()
            print("Update Job: ", job)
            flash('Rekod Job berjaya dikemaskini', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal mengemaskini rekod Job: {str(e)}', 'error')

        return redirect(url_for('show_job_management'))

    # Render the update form with pre-filled data for GET request
    return render_template('update_job.html', job=job)

@app.route('/delete_job/<int:jobNo>', methods=['POST'])
def delete_job_route(jobNo):
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    job = Job.query.get(jobNo)

    if not job:
        flash('Rekod Job tidak dijumpai', 'error')
    else:
        try:
            db.session.delete(job)
            db.session.commit()
            flash('Rekod Job berjaya dipadam', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memadam rekod Job: {str(e)}', 'error')

    return redirect(url_for('show_job_management'))

# Staff Routes
@app.route('/register_staff', methods=['GET', 'POST'])
def register_staff():
    return staff_controller.process_staff_registration()

@app.route('/show_staff_registration_form')
def show_staff_registration_form():
    return staff_controller.show_staff_registration_form()

@app.route('/show_staff_profile')
def show_staff_profile():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses halaman ini', 'error')
        return redirect(url_for('show_login_form'))

    staff_id = session['staff_id']
    staff = Staff.query.filter_by(staffID=staff_id).first()

    if not staff:
        flash('Rekod Staff tidak dijumpai', 'error')
        return redirect(url_for('home'))  # Redirect to home page if staff record not found

    return render_template('staff_profile.html', staff=staff)

@app.route('/update_staff_profile', methods=['POST'])
def update_staff_profile():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    staff_id = session['staff_id']
    staff = Staff.query.filter_by(staffID=staff_id).first()

    if not staff:
        flash('Rekod Staff tidak dijumpai', 'error')
        return redirect(url_for('home'))

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

    return redirect(url_for('show_staff_profile'))
    
# Other routes and functions as needed

# pie chart
@app.route('/get_job_quantities')
def get_job_quantities():
    # Query job data grouped by vehicle type and sum the quantities
    job_data = db.session.query(Job.vehicleType, db.func.sum(Job.quantity)).group_by(Job.vehicleType).all()

    # Prepare data to be sent as JSON
    vehicle_types = [item[0] for item in job_data]
    quantities = [item[1] for item in job_data]

    return jsonify({
        'vehicleTypes': vehicle_types,
        'quantities': quantities
    })

# bar chart 
@app.route('/get_job_costs_profits')
def get_job_costs_profits():
    # Query job data to calculate costs and profits per unit
    job_data = db.session.query(
        Job.vehicleType,
        db.func.avg(Job.costUnit).label('avg_cost_unit'),
        db.func.avg(Job.profitUnit).label('avg_profit_unit')
    ).group_by(Job.vehicleType).all()

    # Prepare data to be sent as JSON
    job_types = [item[0] for item in job_data]
    costs_per_unit = [float(item[1]) if item[1] else 0.0 for item in job_data]
    profits_per_unit = [float(item[2]) if item[2] else 0.0 for item in job_data]

    return jsonify({
        'jobTypes': job_types,
        'costsPerUnit': costs_per_unit,
        'profitsPerUnit': profits_per_unit
    })

# line chart
@app.route('/get_job_profitability_trends')
def get_job_profitability_trends():
    # Query job data sorted by delivery date and collect profits
    job_data = Job.query.order_by(Job.jobDateDelivered).all()

    # Prepare data to be sent as JSON
    job_dates = [job.jobDateDelivered.strftime('%Y-%m-%d') for job in job_data]
    profits = [float(job.totalProfit) for job in job_data]

    return jsonify({
        'jobDates': job_dates,
        'profits': profits
    })

# bar chart
@app.route('/get_aftersales_data')
def get_aftersales_data():
    try:
        # Query aftersales data from the database
        aftersales_data = Aftersales.query.all()

        # Prepare the data to be sent as JSON
        data = [{
            'chassisType': aftersales.chassisType,
            'registrationNo': aftersales.registrationNo,
            'dateDelivered': aftersales.dateDelivered.strftime('%Y-%m-%d'),  # Format date as string
            # Add other relevant fields as needed
        } for aftersales in aftersales_data]

        # Return the aftersales data as JSON response
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error message with 500 status code if an exception occurs