# app\view_home.py

from flask import Flask, jsonify, session, render_template, flash, redirect, url_for
from app.models.aftersales_model import Aftersales
from app.models.job_model import Job
from app.models.sales_model import Sales
from app import db, app
from sqlalchemy import func

@app.route('/combined_view')
def combined_view():
    if 'staff_id' not in session:
        return redirect(url_for('show_login_form'))

    jobs = Job.query.all()
    
    aftersales_data = Aftersales.query.all()
    aftersales_map = {aftersales.jobNo: [] for aftersales in aftersales_data}
    for aftersales in aftersales_data:
        aftersales_map[aftersales.jobNo].append(aftersales)
    
    for job in jobs:
        job.aftersales = aftersales_map.get(job.jobNo, [])

    return render_template('combined_view.html', jobs=jobs)

@app.route('/aftersales_home')
def aftersales_home():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))
    
    staffID = session.get('staff_id')
    return render_template('aftersales_home.html')

@app.route('/sales_marketing_home', methods=['GET'])
def sales_marketing_home():
    if 'staff_id' not in session:  # Ensure the session key matches the login logic
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))
    
    # Calculate overall metrics
    overall_sales = db.session.query(func.sum(Sales.tenderTotalPrice)).scalar() or 0
    overall_profit = db.session.query(func.sum(Sales.tenderTotalProfit)).scalar() or 0
    overall_quantity = db.session.query(func.sum(Sales.quantity)).scalar() or 0
    overall_margin_profit = (overall_profit / (overall_sales - overall_profit)) * 100 if overall_sales > 0 else 0
    
    # Query total sales, total profit, margin profit, and total quantity by salesPerson
    sales_data = db.session.query(
        Sales.salesPerson,
        func.sum(Sales.tenderTotalPrice).label('total_sales'),
        func.sum(Sales.tenderTotalProfit).label('total_profit'),
        func.sum(Sales.quantity).label('total_quantity'),
        ((func.sum(Sales.tenderTotalProfit) / (func.sum(Sales.tenderTotalPrice) - func.sum(Sales.tenderTotalProfit))) * 100).label('margin_profit')
    ).group_by(Sales.salesPerson).all()
    
    return render_template('sales_marketing_home.html', 
                           overall_sales=overall_sales, 
                           overall_profit=overall_profit, 
                           overall_quantity=overall_quantity, 
                           overall_margin_profit=overall_margin_profit, 
                           sales_data=sales_data)

@app.route('/get_combined_job_data')
def get_combined_job_data():
    from sqlalchemy import extract

    job_data = db.session.query(
        extract('year', Job.jobDateDelivered).label('year'),
        db.func.sum(Job.totalSales).label('total_sales'),
        db.func.sum(Job.totalProfit).label('total_profit')
    ).group_by(
        extract('year', Job.jobDateDelivered)
    ).order_by(
        extract('year', Job.jobDateDelivered)
    ).all()

    years = [item.year for item in job_data]
    total_sales = [float(item.total_sales) for item in job_data]
    total_profit = [float(item.total_profit) for item in job_data]
    
    margin_profit = [(profit / (sales - profit) * 100) if (sales - profit) != 0 else 0 
                     for profit, sales in zip(total_profit, total_sales)]

    overall_total_sales = sum(total_sales)
    overall_total_profit = sum(total_profit)
    
    overall_margin_percentage = (overall_total_profit / (overall_total_sales - overall_total_profit) * 100 
                                 if (overall_total_sales - overall_total_profit) != 0 else 0)

    return jsonify({
        'years': years,
        'margin_profit': margin_profit,
        'total_sales': total_sales,
        'total_profit': total_profit,
        'overall_total_sales': overall_total_sales,
        'overall_total_profit': overall_total_profit,
        'overall_margin_percentage': overall_margin_percentage
    })

@app.route('/get_job_profitability_trends')
def get_job_profitability_trends():
    from sqlalchemy import extract

    job_data = db.session.query(
        extract('year', Job.jobDateDelivered).label('year'),
        db.func.sum(Job.totalSales).label('total_sales'),
        db.func.sum(Job.totalProfit).label('total_profit')
    ).group_by(
        extract('year', Job.jobDateDelivered)
    ).order_by(
        extract('year', Job.jobDateDelivered)
    ).all()

    years = [item.year for item in job_data]
    total_sales = [float(item.total_sales) for item in job_data]
    total_profit = [float(item.total_profit) for item in job_data]

    return jsonify({
        'years': years,
        'total_sales': total_sales,
        'total_profit': total_profit
    })

@app.route('/get_job_quantities')
def get_job_quantities():
    job_data = db.session.query(Job.vehicleType, db.func.sum(Job.quantity)).group_by(Job.vehicleType).all()

    vehicle_types = [item[0] for item in job_data]
    quantities = [item[1] for item in job_data]

    return jsonify({
        'vehicleTypes': vehicle_types,
        'quantities': quantities
    })

@app.route('/get_aftersales_data')
def get_aftersales_data():
    try:
        aftersales_data = Aftersales.query.all()

        data = [{
            'chassisType': aftersales.chassisType,
            'registrationNo': aftersales.registrationNo,
            'dateDelivered': aftersales.dateDelivered.strftime('%Y-%m-%d'),
        } for aftersales in aftersales_data]

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-jobs')
def top_jobs():
    top_jobs_data = Job.query.order_by(Job.totalProfit.desc()).limit(5).all()
    top_jobs_list = [
        {"jobNo": job.jobNo, "title": job.title, "custName": job.custName, "totalProfit": job.totalProfit}
        for job in top_jobs_data
    ]
    return jsonify(top_jobs_list)
