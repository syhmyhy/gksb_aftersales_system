# app\view_sales.py

from flask import render_template, redirect, url_for, flash, session
from app.controllers import sales_controller
from app.models.sales_model import Sales
from app import app

@app.route('/sales_form', methods=['GET'])
def show_sales_form():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))
    
    staffID = session.get('staff_id')

    sales_records = Sales.query.all()
    return render_template('sales_form.html', sales_records=sales_records, staffID=staffID)

@app.route('/submit_sales', methods=['POST'])
def submit_sales_form():
    return sales_controller.submit_sales_form()

@app.route('/sales_list', methods=['GET'])
def show_sales_list():
    return sales_controller.show_sales_list()

@app.route('/sales/edit/<int:salesID>', methods=['GET'])
def edit_sales_form(salesID):
    return sales_controller.edit_sales_form(salesID)

@app.route('/sales/update/<int:salesID>', methods=['POST'])
def update_sales_record(salesID):
    return sales_controller.update_sales_record(salesID)

@app.route('/sales/delete/<int:salesID>', methods=['GET'])
def delete_sales_record(salesID):
    return sales_controller.delete_sales_record(salesID)
