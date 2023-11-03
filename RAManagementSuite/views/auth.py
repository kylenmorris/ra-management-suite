from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from RAManagementSuite.repos import userRepo

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

    return render_template('home/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = userRepo.get_user_by_email(email)

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        userRepo.create_user(email, name, password)
        return redirect(url_for('auth.login'))

    return render_template('home/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
