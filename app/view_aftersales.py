# app\view_aftersales.py

from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app.controllers import aftersales_controller
from app.models.aftersales_model import Aftersales
from app.models.job_model import Job
from app import app, db

def prevent_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/aftersales.html')
def show_aftersales_form():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))
    return render_template('aftersales.html')

@app.route('/show_aftersales_management')
def show_aftersales_management():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))

    aftersales_data = Aftersales.query.all()
    return render_template('aftersales_management.html', aftersales_data=aftersales_data)

@app.route('/update_aftersales/<string:registrationNo>', methods=['GET', 'POST'])
def update_aftersales_route(registrationNo):
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
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

            db.session.commit()
            flash('Rekod Aftersales berjaya dikemaskini', 'success')
        except KeyError as e:
            flash(f'Gagal mengemaskini rekod: Ruang diperlukan "{e.args[0]}" hilang', 'error')
        except ValueError as e:
            flash(f'Gagal mengemaskini rekod: Nilai tidak sah untuk medan - {str(e)}', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Ralat semasa mengemaskini rekod: {str(e)}', 'error')

        return redirect(url_for('show_aftersales_management'))

    return render_template('update_aftersales.html', aftersales=aftersales, job=job)

@app.route('/delete_aftersales/<string:registrationNo>', methods=['POST'])
def delete_aftersales_route(registrationNo):
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return jsonify({'success': False, 'message': 'Sila log masuk untuk mengakses laman ini'}), 401

    aftersales = Aftersales.query.filter_by(registrationNo=registrationNo).first()

    if aftersales:
        try:
            job = Job.query.filter_by(jobNo=aftersales.jobNo).first()
            if job:
                job.aftersales_count -= 1
                db.session.delete(aftersales)
                db.session.commit()
                flash('Rekod Aftersales berjaya dipadam', 'success')
                return jsonify({'success': True, 'message': 'Rekod Aftersales berjaya dipadam'}), 200
            else:
                flash('Rekod Aftersales tidak dijumpai', 'error')
                return jsonify({'success': False, 'message': 'Rekod Aftersales tidak dijumpai'}), 404
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memadam rekod Aftersales: {e}', 'error')
            return jsonify({'success': False, 'message': f'Gagal memadam rekod Aftersales: {e}'}), 500
    else:
        flash('Rekod Aftersales tidak dijumpai', 'error')
        return jsonify({'success': False, 'message': 'Rekod Aftersales tidak dijumpai'}), 404

    return redirect(url_for('show_aftersales_management'))

@app.route('/submit_aftersales_form', methods=['POST'])
def submit_aftersales_form():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))
    return aftersales_controller.submit_aftersales_form()
