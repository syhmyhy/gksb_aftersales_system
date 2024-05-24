# app\view_home.py

from flask import Flask, jsonify, session, render_template, make_response, flash, redirect, url_for
from app.models.aftersales_model import Aftersales
from app.models.job_model import Job
from app import db, app
from sqlalchemy import func

def prevent_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'no-store'
    return response

# Home and Main Pages
@app.route('/home.html')
def home():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))
    
    staffID = session.get('staff_id')
    print("Staff ID:", staffID)
    response = make_response(render_template('home.html'))
    return prevent_caching(response)

# pie chart
@app.route('/get_job_quantities')
def get_job_quantities():
    # Query job data grouped by vehicle type and sum the quantities
    job_data = db.session.query(Job.vehicleType, db.func.sum(Job.quantity)).group_by(Job.vehicleType).all()

    # Prepare data to be sent as JSON
    vehicle_types = [item[0] for item in job_data]
    quantities = [item[1] for item in job_data]

    response = make_response(jsonify({
        'vehicleTypes': vehicle_types,
        'quantities': quantities
    }))
    return prevent_caching(response)

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

    response = make_response(jsonify({
        'jobTypes': job_types,
        'costsPerUnit': costs_per_unit,
        'profitsPerUnit': profits_per_unit
    }))
    return prevent_caching(response)

# line chart
@app.route('/get_job_profitability_trends')
def get_job_profitability_trends():
    from sqlalchemy import extract

    # Query job data grouped by year and month, and sum the profits
    job_data = db.session.query(
        extract('year', Job.jobDateDelivered).label('year'),
        extract('month', Job.jobDateDelivered).label('month'),
        db.func.sum(Job.totalProfit).label('monthly_profit')
    ).group_by(
        extract('year', Job.jobDateDelivered),
        extract('month', Job.jobDateDelivered)
    ).order_by(
        extract('year', Job.jobDateDelivered),
        extract('month', Job.jobDateDelivered)
    ).all()

    # Prepare data to be sent as JSON
    job_dates = [f"{item.month:02}/{item.year}" for item in job_data]
    profits = [float(item.monthly_profit) for item in job_data]

    response = make_response(jsonify({
        'jobDates': job_dates,
        'profits': profits
    }))
    return prevent_caching(response)

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
        response = make_response(jsonify(data))
        return prevent_caching(response)
    except Exception as e:
        response = make_response(jsonify({'error': str(e)}), 500)
        return prevent_caching(response)  # Return error message with 500 status code if an exception occurs

@app.route('/api/top-jobs')
def top_jobs():
    # Fetch top 5 most profitable jobs
    top_jobs_data = Job.query.order_by(Job.totalProfit.desc()).limit(5).all()
    top_jobs_list = [
        {"jobNo": job.jobNo, "title": job.title, "custName": job.custName, "totalProfit": job.totalProfit}
        for job in top_jobs_data
    ]
    response = make_response(jsonify(top_jobs_list))
    return prevent_caching(response)