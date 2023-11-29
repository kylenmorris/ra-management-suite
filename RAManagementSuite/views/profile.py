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

# from RAManagementSuite.repos.taskRepo import create_task, get_all_tasks, get_task_by_id, update_task

profile = Blueprint('profile', __name__)


@profile.route('/')
@login_required
def index():
    current_page = 'Profile'
    return render_template('profile/index.html', name=current_user.name, current_page=current_page)

