# app\controllers\sales_controller.py

from flask import request, redirect, url_for, flash, render_template, session
from app import db
from app.models.sales_model import Sales
from app.models.staff_model import Staff  # Add 'Staff' to the import statement
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def submit_sales_form():
    if request.method == 'POST':
        try:
            sales_data = request.form

            new_sales = Sales(
                salesPerson=sales_data['salesPerson'],
                purchaseMethod=sales_data['purchaseMethod'],
                tenderTitle=sales_data['tenderTitle'],
                custName=sales_data['custName'],
                chassisType=sales_data['chassisType'],
                chassisModel=sales_data['chassisModel'],
                quantity=int(sales_data['quantity']),  # Assuming quantity is integer
                tenderDate=sales_data['tenderDate'],
                unitPrice=float(sales_data['unitPrice']),
                tenderTotalPrice=float(sales_data['tenderTotalPrice']),
                unitProfit=float(sales_data['unitProfit']),
                tenderTotalProfit=float(sales_data['tenderTotalProfit']),
                marginProfit=float(sales_data['marginProfit']),
                notes=sales_data['notes'],
                staffID=sales_data['staffID']
            )

            db.session.add(new_sales)
            db.session.commit()
            print("Add Sales: ", new_sales)
            flash('Rekod Sales berjaya ditambah', 'success')
            return render_template('sales_form.html', status='success')

        except (KeyError, ValueError, IntegrityError) as e:
            db.session.rollback()
            error_message = str(e)
            print(f"Failed to add Sales: {error_message}")  # Detailed error message
            flash(f'Gagal menambah rekod Sales. Sila lengkapkan semua ruang.', 'error')
            return render_template('sales_form.html', status='error')

    return redirect(url_for('show_sales_form'))

def show_sales_list():
    sales_data = Sales.query.all()
    return render_template('sales_list.html', sales_data=sales_data)

def edit_sales_form(salesID):
    sale = Sales.query.get(salesID)
    if not sale:
        flash('Rekod Jualan Tidak Dijumpai', 'error')
        return redirect(url_for('show_sales_list'))

    return render_template('update_sales.html', sale=sale)

def update_sales_data(salesID):
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))

    sales = Sales.query.get(salesID)

    if not sales:
        flash('Rekod Jualan Tidak Dijumpai', 'error')
        return redirect(url_for('show_sales_list'))

    if request.method == 'POST':
        try:
            sales.salesPerson = request.form['salesPerson']
            sales.purchaseMethod = request.form['purchaseMethod']
            sales.tenderTitle = request.form['tenderTitle']
            sales.custName = request.form['custName']
            sales.chassisType = request.form['chassisType']
            sales.chassisModel = request.form['chassisModel']
            sales.quantity = int(request.form['quantity'])
            sales.tenderDate = request.form['tenderDate']
            sales.unitPrice = float(request.form['unitPrice'])
            sales.tenderTotalPrice = float(request.form['tenderTotalPrice'])
            sales.unitProfit = float(request.form['unitProfit'])
            sales.tenderTotalProfit = float(request.form['tenderTotalProfit'])
            sales.marginProfit = float(request.form['marginProfit'])
            sales.notes = request.form['notes']

            db.session.commit()
            print("Update Sales: ", sales)
            flash('Rekod Jualan berjaya dikemaskini', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Gagal mengemaskini rekod Jualan: {str(e)}', 'error')

        return redirect(url_for('show_sales_list'))

    return render_template('update_sales.html', sales=sales)

def delete_sales_data(salesID):
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))
    
    sales = Sales.query.get(salesID)
    
    if not sales:
        flash('Rekod Jualan tidak dijumpai', 'error')
    else:
        try:
            db.session.delete(sales)
            db.session.commit()
            flash('Rekod Jualan berjaya dipadam', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memadam rekod Jualan: {str(e)}', 'error')
    
    return redirect(url_for('show_sales_list'))