# app\view_auth.py

from flask import render_template, request, redirect, url_for, session, make_response, flash
from app.controllers import auth_controller
from app import app

def prevent_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'no-store'
    return response

# Authentication Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'staff_id' in session:
        # If user is logged in, redirect to home page
        return redirect(url_for('home'))

    if request.method == 'POST':
        return auth_controller.login()
    else:
        return auth_controller.show_login_form()

@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    flash('Anda telah berjaya log keluar', 'success')
    return redirect(url_for('show_login_form'))

@app.route('/show_login_form')
def show_login_form():
    if 'staff_id' in session:
        return redirect(url_for('home'))  # Redirect to home if already logged in
    return auth_controller.show_login_form()

# Other routes and functions as needed