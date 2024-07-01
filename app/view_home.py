# app\view_home.py

from flask import Flask, jsonify, session, render_template, flash, redirect, url_for, request
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

    selected_year = request.args.get('year')

    # Calculate overall metrics by year
    metrics_by_year = db.session.query(
        func.date_format(Job.jobDateDelivered, '%Y').label('year'),
        func.sum(Job.totalSales).label('overall_sales'),
        func.sum(Job.totalProfit).label('overall_profit'),
        func.sum(Job.quantity).label('overall_quantity')
    ).group_by('year').all()

    overall_metrics_by_year = {}
    total_sales = 0
    total_profit = 0
    total_quantity = 0

    for year, overall_sales, overall_profit, overall_quantity in metrics_by_year:
        overall_sales = overall_sales or 0
        overall_profit = overall_profit or 0
        overall_quantity = overall_quantity or 0
        overall_margin_profit = (overall_profit / (overall_sales - overall_profit)) * 100 if overall_sales > 0 else 0
        overall_metrics_by_year[year] = {
            'overall_sales': overall_sales,
            'overall_profit': overall_profit,
            'overall_quantity': overall_quantity,
            'overall_margin_profit': overall_margin_profit
        }
        total_sales += overall_sales
        total_profit += overall_profit
        total_quantity += overall_quantity
    
    total_margin_profit = (total_profit / (total_sales - total_profit)) * 100 if total_sales > 0 else 0

    # Sort the overall_metrics_by_year dictionary by year
    overall_metrics_by_year = dict(sorted(overall_metrics_by_year.items()))

    if selected_year and selected_year in overall_metrics_by_year:
        filtered_metrics = {selected_year: overall_metrics_by_year[selected_year]}
    else:
        filtered_metrics = overall_metrics_by_year

    return render_template('aftersales_home.html', 
                           overall_metrics_by_year=filtered_metrics,
                           total_sales=total_sales,
                           total_profit=total_profit,
                           total_quantity=total_quantity,
                           total_margin_profit=total_margin_profit,
                           years=overall_metrics_by_year.keys(),
                           selected_year=selected_year)


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

# @app.route('/get_job_profitability_trends')
# def get_job_profitability_trends():
#     from sqlalchemy import extract

#     job_data = db.session.query(
#         extract('year', Job.jobDateDelivered).label('year'),
#         db.func.sum(Job.totalSales).label('total_sales'),
#         db.func.sum(Job.totalProfit).label('total_profit')
#     ).group_by(
#         extract('year', Job.jobDateDelivered)
#     ).order_by(
#         extract('year', Job.jobDateDelivered)
#     ).all()

#     years = [item.year for item in job_data]
#     total_sales = [float(item.total_sales) for item in job_data]
#     total_profit = [float(item.total_profit) for item in job_data]

#     return jsonify({
#         'years': years,
#         'total_sales': total_sales,
#         'total_profit': total_profit
#     })

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
