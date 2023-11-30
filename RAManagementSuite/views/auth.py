from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

from repos import userRepo, signupCodeRepo

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = userRepo.get_user_by_email(email)

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('home.profile'))  # or wherever you want to redirect after a successful login

    return render_template('auth/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        form_code = request.form.get('signup-code')
        signup_code = signupCodeRepo.get_signup_code(form_code)

        # this could be one if statement but this way we get more descriptive error messages
        if not signup_code:
            flash('Code not found')
            return redirect(url_for('auth.signup'))
        if signup_code.used:
            flash('Code already used')
            return redirect(url_for('auth.signup'))
        # if it was created more than a week ago
        if (signup_code.created + timedelta(days=7)) < (datetime.now()):
            flash('Code has expired')
            return redirect(url_for('auth.signup'))

        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = userRepo.get_user_by_email(email)

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        userRepo.create_user(email, name, password)

        # mark the code as used
        signupCodeRepo.update_signup_code(signup_code.id, True)

        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('auth/logout.html')
