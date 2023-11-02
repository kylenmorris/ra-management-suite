from flask import Blueprint, render_template, request, redirect, url_for, flash
# Additional imports for authentication will go here...

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('home/login.html')

@auth.route('/signup')
def signup():
    return render_template('home/signup.html')

@auth.route('/logout')
def logout():
    return render_template('home/logout.html')

