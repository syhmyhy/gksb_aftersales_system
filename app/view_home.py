# app\view_home.py

from flask import Flask, jsonify, session, render_template
from app.models.aftersales_model import Aftersales
from app.models.job_model import Job
from app import db, app
from sqlalchemy import func

@app.route('/combined_view')
def combined_view():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    jobs = Job.query.all()
    
    # Pre-fetch aftersales data and map it to jobNo for easy access
    aftersales_data = Aftersales.query.all()
    aftersales_map = {}
    for aftersales in aftersales_data:
        if aftersales.jobNo not in aftersales_map:
            aftersales_map[aftersales.jobNo] = []
        aftersales_map[aftersales.jobNo].append(aftersales)
    
    # Attach the aftersales data to the respective jobs
    for job in jobs:
        job.aftersales = aftersales_map.get(job.jobNo, [])

    return render_template('combined_view.html', jobs=jobs)

# Home and Main Pages
@app.route('/home.html')
def home():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))
    
    staffID = session.get('staff_id')
    print("Staff ID:", staffID)
    return render_template('home.html')

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
@app.route('/get_job_sales_profits')
def get_job_sales_profits():
    # Query job data to calculate sales and profits per unit
    job_data = db.session.query(
        Job.vehicleType,
        db.func.avg(Job.salesUnit).label('avg_sales_unit'),
        db.func.avg(Job.profitUnit).label('avg_profit_unit')
    ).group_by(Job.vehicleType).all()

    # Prepare data to be sent as JSON
    job_types = [item[0] for item in job_data]
    sales_per_unit = [float(item[1]) if item[1] else 0.0 for item in job_data]
    profits_per_unit = [float(item[2]) if item[2] else 0.0 for item in job_data]

    return jsonify({
        'jobTypes': job_types,
        'salesPerUnit': sales_per_unit,
        'profitsPerUnit': profits_per_unit
    })

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

@app.route('/api/top-jobs')
def top_jobs():
    # Fetch top 5 most profitable jobs
    top_jobs_data = Job.query.order_by(Job.totalProfit.desc()).limit(5).all()
    top_jobs_list = [
        {"jobNo": job.jobNo, "title": job.title, "custName": job.custName, "totalProfit": job.totalProfit}
        for job in top_jobs_data
    ]
    return jsonify(top_jobs_list)
