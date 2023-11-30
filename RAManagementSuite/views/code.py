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

code = Blueprint('code', __name__)


@code.route('/create', methods=['POST'])
@login_required
def create():
    signupCodeRepo.create_signup_code()
    return redirect(url_for('user.index'))


@code.route('/delete/<int:code_id>', methods=['POST'])
@login_required
def delete(code_id):
    signupCodeRepo.delete_signup_code(code_id)
    return redirect(url_for('user.index'))


# for code in all_codes:
#     code.formatted_created = code.created.strftime('%b %d, %Y')
#     code.formatted_expires = (code.created + timedelta(days=7)).strftime('%b %d, %Y')  # week after creation