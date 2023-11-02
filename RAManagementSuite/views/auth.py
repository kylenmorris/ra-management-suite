from flask import Blueprint, render_template, request, redirect, url_for, flash
from RAManagementSuite.repos import userRepo

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
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
def logout():
    return render_template('home/logout.html')

