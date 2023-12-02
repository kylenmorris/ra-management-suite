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

user = Blueprint('user', __name__)


@user.route('/')
@login_required
def index():
    if current_user.role.value != "Coordinator":
        abort(403, "ERROR 403: Current users does not have required access level")
    else:
        current_page = 'Users'
        all_users = userRepo.get_all_users()
        all_roles = userRepo.get_roles_values()

        return render_template('user/index.html', users=all_users, roles=all_roles,
                               current_page=current_page, UserRole=UserRole)


@user.route('/change-role/<int:user_id>', methods=['POST'])
@login_required
def change_role(user_id):
    if current_user.role.value != "Coordinator":
        abort(403, "ERROR 403: Current users does not have required access level")
    else:
        new_role = request.form.get('role')
        userRepo.change_user_role(user_id, new_role)
        return redirect(url_for('user.index'))

@user.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete(user_id):
    if current_user.role.value != "Coordinator":
        abort(403, "ERROR 403: Current users does not have required access level")
    else:
        userRepo.delete_user(user_id)
        return redirect(url_for('user.index'))
