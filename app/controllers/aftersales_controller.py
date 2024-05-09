# app\controllers\aftersales_controller.py

from flask import render_template, request, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Aftersales, Job

def show_aftersales_form():
    return render_template('aftersales.html')

def submit_aftersales_form():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    if request.method == 'POST':
        try:
            aftersales_data = request.form

            jobNo = int(aftersales_data['jobNo'])
            job = Job.query.filter_by(jobNo=jobNo).first()

            if not job:
                flash('Rekod Job tidak dijumpai', 'error')
                return redirect(url_for('show_aftersales_form'))

            # Check if adding this aftersales record will exceed the quantity limit
            if job.aftersales_count + 1 > job.quantity:
                flash('Kuantiti aftersales untuk Job ini telah mencapai had', 'error')
                return redirect(url_for('show_aftersales_form'))

            new_aftersales = Aftersales(
                jobNo=jobNo,
                endUser=aftersales_data['endUser'],
                bodyType=aftersales_data['bodyType'],
                chassisType=aftersales_data['chassisType'],
                chassisModel=aftersales_data['chassisModel'],
                chassisNo=aftersales_data['chassisNo'],
                engineNo=aftersales_data['engineNo'],
                registrationNo=aftersales_data['registrationNo'],
                dateDelivered=aftersales_data['dateDelivered'],
                stateLocality=aftersales_data['stateLocality'],
                detailLocality=aftersales_data['detailLocality'],
                chassisMileageWarranty=int(aftersales_data['chassisMileageWarranty']),
                chassisPeriodWarranty=int(aftersales_data['chassisPeriodWarranty']),
                chassisExpired=aftersales_data['chassisExpired'],
                bodyPeriodWarranty=int(aftersales_data['bodyPeriodWarranty']),
                bodyExpired=aftersales_data['bodyExpired'],
                noService=int(aftersales_data['noService']),
                mileageService=int(aftersales_data['mileageService']),
                custPhone=aftersales_data.get('custPhone'),
                custEmail=aftersales_data.get('custEmail'),
                notes=aftersales_data.get('notes'),
            )

            db.session.add(new_aftersales)
            db.session.commit()

            # Update aftersales_count for the associated Job
            job.aftersales_count += 1
            db.session.commit()

            flash('Rekod Aftersales berjaya ditambah', 'success')
            return redirect(url_for('show_aftersales_form'))

        except IntegrityError as e:
            db.session.rollback()
            error_info = str(e.orig)
            if 'Duplicate entry' in error_info:
                flash('Rekod Aftersales sudah wujud', 'error')
            else:
                flash('Gagal menambah rekod Aftersales. Sila semak masukan anda.', 'error')

            return redirect(url_for('show_aftersales_form'))

    return redirect(url_for('show_aftersales_form'))

def get_all_aftersales():
    aftersales_data = Aftersales.query.all()
    print("Total Aftersales records:", len(aftersales_data))
    return aftersales_data

# Other functions related to aftersales_controller.py if needed