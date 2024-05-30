# app\view_home.py

from flask import Flask, jsonify, session, render_template, flash, redirect,url_for
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

# chart number 1
@app.route('/get_combined_job_data')
def get_combined_job_data():
    from sqlalchemy import extract

    # Query job data grouped by year and calculate total sales, total profit, and margin profit for the year
    job_data = db.session.query(
        extract('year', Job.dateReceived).label('year'),
        db.func.sum(Job.totalSales).label('total_sales'),
        db.func.sum(Job.totalProfit).label('total_profit')
    ).group_by(
        extract('year', Job.dateReceived)
    ).order_by(
        extract('year', Job.dateReceived)
    ).all()

    # Calculate the margin profit for each year with the updated formula
    years = [item.year for item in job_data]
    total_sales = [float(item.total_sales) for item in job_data]
    total_profit = [float(item.total_profit) for item in job_data]
    
    # Adjusted formula for margin profit calculation
    margin_profit = [(profit / (sales - profit) * 100) if (sales - profit) != 0 else 0 
                     for profit, sales in zip(total_profit, total_sales)]

    return jsonify({
        'years': years,
        'margin_profit': margin_profit,
        'total_sales': total_sales,
        'total_profit': total_profit
    })

# line chart number 2
@app.route('/get_job_profitability_trends')
def get_job_profitability_trends():
    from sqlalchemy import extract

    # Query job data grouped by year and sum the sales and profits
    job_data = db.session.query(
        extract('year', Job.dateReceived).label('year'),
        db.func.sum(Job.totalSales).label('total_sales'),
        db.func.sum(Job.totalProfit).label('total_profit')
    ).group_by(
        extract('year', Job.dateReceived)
    ).order_by(
        extract('year', Job.dateReceived)
    ).all()

    # Prepare data to be sent as JSON
    years = [item.year for item in job_data]
    total_sales = [float(item.total_sales) for item in job_data]
    total_profit = [float(item.total_profit) for item in job_data]

    return jsonify({
        'years': years,
        'total_sales': total_sales,
        'total_profit': total_profit
    })

# pie chart number 3
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

# bar chart number 4
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
