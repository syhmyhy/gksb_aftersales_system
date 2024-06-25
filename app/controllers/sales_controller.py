# app\controllers\sales_controller.py

from flask import request, redirect, url_for, flash, render_template, session
from app import db
from app.models.sales_model import Sales
from app.models.staff_model import Staff  # Add 'Staff' to the import statement
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def submit_sales_form():
    sales_data = request.form

    staffID = session.get('staffID')

    # Check if staffID exists in the staff table
    staff = Staff.query.filter_by(staffID=staffID).first()
    if not staff:
        flash(f'Staff ID {staffID} not found in database', 'error')
        return redirect(url_for('show_sales_list'))

    new_sale = Sales(
        # Remove salesID since it will be auto-incremented
        salesPerson=sales_data['salesPerson'],
        purchaseMethod=sales_data['purchaseMethod'],
        tenderTitle=sales_data['tenderTitle'],
        custName=sales_data.get('custName'),
        chassisType=sales_data.get('chassisType'),
        chassisModel=sales_data.get('chassisModel'),
        quantity=int(sales_data['quantity']),
        tenderDate=datetime.strptime(sales_data['tenderDate'], '%Y-%m-%d').date(),
        unitPrice=float(sales_data['unitPrice']),
        tenderTotalPrice=float(sales_data.get('tenderTotalPrice', 0.0)),
        unitProfit=float(sales_data.get('unitProfit', 0.0)),
        tenderTotalProfit=float(sales_data.get('tenderTotalProfit', 0.0)),
        marginProfit=float(sales_data.get('marginProfit', 0.0)),
        notes=sales_data.get('notes', ''),
        staffID=staffID
    )

    try:
        db.session.add(new_sale)
        db.session.commit()
        flash('New sales record added successfully', 'success')
    except (KeyError, ValueError, IntegrityError) as e:
        db.session.rollback()
        flash(f'Failed to add new sales record: {str(e)}', 'error')

    return redirect(url_for('show_sales_list'))
def show_sales_list():
    sales_records = Sales.query.all()
    return render_template('sales_list.html', sales_records=sales_records)

def edit_sales_form(salesID):
    sale = Sales.query.get(salesID)
    if not sale:
        flash('Sales record not found', 'error')
        return redirect(url_for('show_sales_list'))

    return render_template('update_sales.html', sale=sale)

def update_sales_record(salesID):
    sale = Sales.query.get(salesID)
    if not sale:
        flash('Sales record not found', 'error')
        return redirect(url_for('show_sales_list'))

    sales_data = request.form

    sale.salesPerson = sales_data['salesPerson']
    sale.purchaseMethod = sales_data['purchaseMethod']
    sale.tenderTitle = sales_data['tenderTitle']
    sale.custName = sales_data.get('custName')
    sale.chassisType = sales_data.get('chassisType')
    sale.chassisModel = sales_data.get('chassisModel')
    sale.quantity = int(sales_data['quantity'])
    sale.tenderDate = datetime.strptime(sales_data['tenderDate'], '%Y-%m-%d').date()
    sale.unitPrice = float(sales_data['unitPrice'])
    sale.tenderTotalPrice = float(sales_data.get('tenderTotalPrice', 0.0))
    sale.unitProfit = float(sales_data.get('unitProfit', 0.0))
    sale.tenderTotalProfit = float(sales_data.get('tenderTotalProfit', 0.0))
    sale.marginProfit = float(sales_data.get('marginProfit', 0.0))
    sale.notes = sales_data.get('notes', '')

    try:
        db.session.commit()
        flash('Sales record successfully updated', 'success')
    except (KeyError, ValueError, IntegrityError) as e:
        db.session.rollback()
        flash(f'Failed to update sales record: {str(e)}', 'error')

    return redirect(url_for('show_sales_list'))

def delete_sales_record(salesID):
    sale = Sales.query.get(salesID)
    if not sale:
        flash('Sales record not found', 'error')
    else:
        try:
            db.session.delete(sale)
            db.session.commit()
            flash('Sales record successfully deleted', 'success')
        except IntegrityError as e:
            db.session.rollback()
            flash(f'Failed to delete sales record: {str(e)}', 'error')

    return redirect(url_for('show_sales_list'))
