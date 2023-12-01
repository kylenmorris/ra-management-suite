import os
from datetime import datetime

from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect, jsonify, abort
from flask_login import login_required, current_user
from models import UserRole
from models import Event
from datetime import datetime, timedelta
from repos import announcementRepo, signupCodeRepo
from repos.eventRepo import create_event, get_all_events, update_event, delete_event
from repos import userRepo

from models import Event, UserRole, TaskPriority, User, TaskStatus, EventType
from repos import announcementRepo, taskRepo
from repos.eventRepo import create_event, get_all_events, update_event, delete_event
from repos.userRepo import update_user_profile, get_user_profile, get_user_by_id

# from RAManagementSuite.repos.taskRepo import create_task, get_all_tasks, get_task_by_id, update_task

profile = Blueprint('profile', __name__)


@profile.route('/', methods=['GET', 'POST'])
@login_required
def index():
    current_page = 'Profile'

    if request.method == 'POST':
        # Extract data from form and update the profile
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        gender = request.form.get('gender')
        pronouns = request.form.get('pronouns')
        availability = request.form.get('availability')
        update_user_profile(current_user.id, name, phone_number, gender, pronouns, availability)

    user_profile = get_user_profile(current_user.id)
    return render_template('profile/index.html', current_user=current_user, user=current_user,
                           profile=user_profile, current_page=current_page)


@profile.route('/view/<int:user_id>')
@login_required
def view(user_id):
    current_page = 'Profile'
    user = get_user_by_id(user_id)
    profile = get_user_profile(user_id)
    return render_template('profile/index.html', profile=profile, current_page=current_page,
                           user=user, current_user=current_user)
