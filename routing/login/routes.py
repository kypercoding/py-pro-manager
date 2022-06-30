from flask import Blueprint, render_template, redirect, request, url_for, current_app, session
from flask_login import login_required, login_manager, login_user

from db import user_db as udb
from .user import User
from auth import validate_user_input as vui


login_bp = Blueprint(
    "login_bp",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@login_bp.route('/', methods=['GET'])
def landing():
    """
    Renders the landing page.
    """
    return redirect('/login')


@login_bp.route('/register', methods=['GET', 'POST'])
def registration(error=None):
    """
    Renders the registration page.
    """
    if request.method == 'POST':
        # get username, email, and password
        # from form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # get error, if any, from validating username
        error = vui.validate_username(username)

        # return username-related errors if necessary
        if error != None:
            return render_template('login/registration.html', error=error)
        
        # get error, if any, from validating password
        error = vui.validate_password(password)

        # if the password incurs an error, then
        # send the user an error message
        if error != None:
            return render_template('login/registration.html', error=error)
        
        # get error, if any, from validating email
        error = vui.validate_email(password)

        # if the email incurs an error, then
        # send the user an error message
        if error != None:
            return render_template('login/registration.html', error=error)

        if udb.register(username, email, password, current_app.config['db']):
            return redirect('/')
        else:
            error = "Unknown error occured, please try again"
            return render_template('login/registration.html', error=error)
    
    return render_template('login/registration.html', error=error)


@login_bp.route('/login', methods=['GET', 'POST'])
def login(error=None):
    if request.method == 'POST':
        # get username and password from login form
        username = request.form.get('username')
        password = request.form.get('password')

        # retrieves error, if any, returned by
        # checking input
        error = vui.check_user_and_pass(username, password)

        # sends user an error message regarding invalid
        # text input
        if error != None:
            return render_template('login/login.html', error=error)

        # validates user against database
        if udb.validate_user(username, password, current_app.config['db']):
            # logs user into application
            data = udb.get_by_user(username, current_app.config['db'])
            login_user(User(data['uuid'], data['username'], data['email']))

            return redirect('/home')
        else:
            error = "Invalid username and/or password, please try again!"
    
    return render_template('login/login.html', error=error)
