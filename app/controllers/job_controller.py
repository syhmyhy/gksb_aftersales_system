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
                jobNo=int(job_data['jobNo']),
                title=job_data['title'],
                custName=job_data['custName'],
                vehicleType=job_data['vehicleType'],
                quantity=int(job_data['quantity']),
                dateReceived=job_data['dateReceived'],
                costUnit=float(job_data['costUnit']),
                totalCost=float(job_data['totalCost']),
                profitUnit=float(job_data['profitUnit']),
                totalProfit=float(job_data['totalProfit']),
                jobDateDelivered=job_data['jobDateDelivered'],
                staffID=int(job_data['staffID'])
            )

            db.session.add(new_job)
            db.session.commit()
            print("Job Added")
            flash('Rekod Job berjaya ditambah', 'success')  # Mesej kejayaan dalam Bahasa Melayu
            return render_template('job.html', status='success')

        except (KeyError, ValueError, IntegrityError) as e:
            db.session.rollback()
            print("Failed to add Job")
            flash('Gagal menambah rekod Job. Sila semak masukan anda.', 'error')  # Mesej ralat dalam Bahasa Melayu
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
    job_data = Job.query.all()  # Retrieve all job records
    print("Total Job records:", len(job_data))
    return job_data