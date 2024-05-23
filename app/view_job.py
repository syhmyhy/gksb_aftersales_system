# app\view_job.py

from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash, jsonify
from app.controllers import job_controller
from app.models.job_model import Job
from app import app, db

def prevent_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'no-store'
    return response

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
