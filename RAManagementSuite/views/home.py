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

home = Blueprint('home', __name__)


@home.route('/')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    current_page = 'home'
    announcements = announcementRepo.get_announcements()
    tasks = taskRepo.get_tasks_by_user(current_user.id)
    return render_template('home/index.html', announcements=announcements, tasks=tasks,
                           TaskPriority=TaskPriority, current_page=current_page)
