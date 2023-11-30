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

task = Blueprint('task', __name__)


@task.route('/', methods=['GET'])
@login_required
def index():
    current_page = 'Tasks'
    if current_user.role == UserRole.BASIC:
        # If the user is basic, show only tasks assigned to them
        tasks = taskRepo.get_tasks_by_user(current_user.id)
    else:
        # If the user has higher privileges, show all tasks
        tasks = taskRepo.get_all_tasks()

    return render_template('task/index.html', tasks=tasks, UserRole=UserRole, current_page=current_page)


@task.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    current_page = 'Tasks'
    # Check if the user has permission to create tasks
    if current_user.role == UserRole.BASIC:
        flash('You do not have permission to create tasks.')
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        priority = request.form.get('priority')
        assigned_user_ids = request.form.getlist('assigned_users')

        taskRepo.create_task(title, description, deadline, TaskPriority[priority.upper()],
                             current_user.id, assigned_user_ids)
        flash('Task created successfully!')
        return redirect(url_for('task.index'))

    users = User.query.all()
    return render_template('task/create.html', users=users, current_page=current_page)


@task.route('/edit/<int:task_id>/', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    current_page = 'Tasks'
    # Check if the user has permission to edit tasks
    if current_user.role == UserRole.BASIC:
        flash('You do not have permission to edit tasks.')
        return redirect(url_for('task.index'))

    task = taskRepo.get_task_by_id(task_id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        priority = request.form.get('priority')
        status = request.form.get('status')
        assigned_user_ids = request.form.getlist('assigned_users')

        taskRepo.update_task(task_id, title, description, deadline, TaskPriority[priority.upper()],
                             TaskStatus[status.upper()], assigned_user_ids)
        flash('Task updated successfully!')
        return redirect(url_for('task.index'))

    users = User.query.all()
    return render_template('task/edit.html', task=task, users=users, current_page=current_page)


@task.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    # Check if the user has permission to delete tasks
    if current_user.role == UserRole.BASIC:
        flash('You do not have permission to delete tasks.')
        return redirect(url_for('task.index'))

    try:
        taskRepo.delete_task(task_id)
        flash('Task deleted successfully.')
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('task.index'))


@task.route('/update_status/<int:task_id>', methods=['POST'])
@login_required
def update_status(task_id):
    if current_user.role != UserRole.BASIC:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('task.index'))

    new_status = request.form.get('status')

    try:
        task = taskRepo.get_task_by_id(task_id)
        if task:
            taskRepo.update_task_status(task_id, TaskStatus[new_status.upper()])
            flash('Task status updated successfully.')
    except ValueError as e:
        flash(str(e))

    return redirect(url_for('task.index'))
