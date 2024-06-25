# app\view_auth.py

from flask import render_template, request, redirect, url_for, session, flash
from app.controllers import auth_controller
from app import app

def prevent_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'staff_id' in session:
        return redirect(url_for('select_page'))

    if request.method == 'POST':
        return auth_controller.login()
    else:
        return auth_controller.show_login_form()

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah berjaya log keluar', 'success')
    return redirect(url_for('show_login_form'))

@app.route('/show_login_form')
def show_login_form():
    if 'staff_id' in session:
        return redirect(url_for('select_page'))
    return auth_controller.show_login_form()

@app.route('/select_page')
def select_page():
    if 'staff_id' not in session:
        flash('Sila log masuk untuk mengakses laman ini', 'error')
        return redirect(url_for('show_login_form'))
    return render_template('select_page.html')
