# app\controllers\job_controller.py

from flask import render_template, request, redirect, url_for, jsonify, flash
from app import db
from app.models.job_model import Job
from sqlalchemy.exc import IntegrityError

def show_job_form():
    jobs = Job.query.all()
    return render_template('job.html', jobs=jobs)

def submit_job_form():
    if request.method == 'POST':
        try:
            job_data = request.form

            new_job = Job(
                jobNo=job_data['jobNo'],  # No need to convert to int
                title=job_data['title'],
                custName=job_data['custName'],
                vehicleType=job_data['vehicleType'],
                quantity=float(job_data['quantity']),
                dateReceived=job_data['dateReceived'],
                salesUnit=float(job_data['salesUnit']),
                totalSales=float(job_data['totalSales']),
                profitUnit=float(job_data['profitUnit']),
                totalProfit=float(job_data['totalProfit']),
                marginProfit=float(job_data['marginProfit']),
                jobDateDelivered=job_data['jobDateDelivered'],
                staffID=job_data['staffID']
            )

            db.session.add(new_job)
            db.session.commit()
            print("Add Job: ", new_job)
            flash('Rekod Job berjaya ditambah', 'success')
            return render_template('job.html', status='success')

        except (KeyError, ValueError, IntegrityError) as e:
            db.session.rollback()
            error_message = str(e)
            print(f"Failed to add Job: {error_message}")  # Detailed error message
            flash(f'Gagal menambah rekod Job. Sila lengkapkan semua ruang.', 'error')
            return render_template('job.html', status='error')

    return redirect(url_for('show_job_form'))

def get_job_details(job_no):
    job = Job.query.filter_by(jobNo=job_no).first()
    if job:
        return jsonify({
            'title': job.title,
            'custName': job.custName,
            'vehicleType': job.vehicleType,
        })
    else:
        return jsonify({'error': 'Job tidak dijumpai'}), 404

def get_all_job():
    job_data = Job.query.all()
    print("Total Job records:", len(job_data))
    return job_data