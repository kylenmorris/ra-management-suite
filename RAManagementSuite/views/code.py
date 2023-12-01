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


@code.route('/')
@login_required
def index():
    if current_user.role.value != "Coordinator":
        abort(403, "ERROR 403: Current users does not have required access level")
    else:
        current_page = 'Codes'
        all_codes = signupCodeRepo.get_signup_codes()

        # it is irritatingly hard to do this through the db so just populate it on the get
        for code in all_codes:
            code.formatted_created = code.created.strftime('%b %d, %Y')
            code.formatted_expires = (code.created + timedelta(days=7)).strftime('%b %d, %Y')  # week after creation

        return render_template('code/index.html', all_codes=all_codes,
                               current_page=current_page, UserRole=UserRole)


@code.route('/create', methods=['POST'])
@login_required
def create():
    signupCodeRepo.create_signup_code()
    return redirect(url_for('code.index'))


@code.route('/delete/<int:code_id>', methods=['POST'])
@login_required
def delete(code_id):
    signupCodeRepo.delete_signup_code(code_id)
    return redirect(url_for('code.index'))


# for code in all_codes:
#     code.formatted_created = code.created.strftime('%b %d, %Y')
#     code.formatted_expires = (code.created + timedelta(days=7)).strftime('%b %d, %Y')  # week after creation
