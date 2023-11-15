import os
from datetime import datetime

from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import login_required, current_user
from models import UserRole
from models import Event
from repos import announcementRepo
from repos.eventRepo import create_event, get_all_events, update_event, delete_event
from repos import userRepo

from models import Event, UserRole, TaskPriority, User, TaskStatus, EventType
from repos import announcementRepo, taskRepo
from repos.eventRepo import create_event, get_all_events, update_event, delete_event

# from RAManagementSuite.repos.taskRepo import create_task, get_all_tasks, get_task_by_id, update_task

home = Blueprint('home', __name__)


@home.route('/')
def index():
    current_page = 'home'
    announcements = announcementRepo.get_announcements()
    return render_template('home/index.html', announcements=announcements, current_page=current_page)


@home.route('/announcement')
def announcement_page():
    current_page = 'announcement_page'
    announcements = announcementRepo.get_announcements()
    return render_template('home/announcement.html', announcements=announcements, current_page=current_page, UserRole=UserRole)

@home.route('/view/<int:announcement_id>')
def announcement(announcement_id):
    current_page = 'announcement_page'
    announcement = announcementRepo.get_announcement(announcement_id)
    return render_template('home/view.html', announcement=announcement, UserRole=UserRole, current_page=current_page)


@home.route('/create', methods=('GET', 'POST'))
def create():
    current_page = 'announcement_page'
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            announcementRepo.create_announcement(title, content, current_user.id)
            return redirect(url_for('home.announcement_page'))

    return render_template('home/create.html', current_page=current_page)


@home.route('/edit/<int:announcement_id>/', methods=('GET', 'POST'))
def edit(announcement_id):
    current_page = 'announcement_page'
    announcement = announcementRepo.get_announcement(announcement_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            announcementRepo.edit_announcement(title, content, announcement_id)
            return redirect(url_for('home.announcement_page'))

    return render_template('home/edit.html', announcement=announcement, current_page=current_page)


@home.route('/delete/<int:announcement_id>/')
def delete_announcement(announcement_id):
    announcementRepo.del_announcement(announcement_id)
    return redirect(url_for('home.announcement_page'))


@home.route('/profile')
@login_required
def profile():
    current_page = 'Profile'
    return render_template('home/profile.html', name=current_user.name, current_page=current_page)


@home.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    current_page = 'Calendar'
    if request.method == 'POST':
        # get data from form and create or update an event
        title = request.form.get('title')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        color = request.form.get('color')
        description = request.form.get('description')
        event_id = request.form.get('event_id')
        event_type = request.form.get(
            'event_type') if current_user.role == UserRole.COORDINATOR else EventType.NORMAL
        assigned_user_id = request.form.get('assigned_user_id') if current_user.role == UserRole.COORDINATOR else None

        if assigned_user_id == "None" or assigned_user_id == "":
            assigned_user_id = None

        if event_id and event_id.strip() != '':
            update_event(event_id, title, start_date, end_date, color, description, event_type, assigned_user_id)
        else:
            create_event(title, start_date, end_date, current_user.id, color, description, event_type, assigned_user_id)
        return redirect(url_for('home.events'))

    events = get_all_events()
    users = User.query.all()
    # Filter events by type if a toggle is set, this should correspond to a filter in your frontend
    filter_type = request.args.get('type')
    if filter_type:
        events = [event for event in events if event.event_type == filter_type]

    return render_template('home/events.html', events=events, current_user=current_user,
                           EventType=EventType, UserRole=UserRole, users=users, current_page=current_page)


@home.route('/api/events', methods=['GET'])
@login_required
def get_events():
    # Optionally handle a filter for event types
    event_type_filter = request.args.get('event_type')

    query = Event.query
    if event_type_filter:
        query = query.filter_by(event_type=event_type_filter)

    events = query.all()
    events_data = [{
        'id': event.id,
        'title': event.title,
        'start': event.start_date.isoformat(),
        'end': event.end_date.isoformat(),
        'color': event.color,
        'description': event.description,
        'event_type': event.event_type.value,
        'assigned_user_id': event.assigned_user_id,
        'assigned_user': {
            'id': event.assigned_user.id,
            'name': event.assigned_user.name
        } if event.assigned_user else None,  # Serialize the user here
        'ownerId': event.owner_id
    } for event in events]

    return jsonify(events_data)


@home.route('/delete-event/<int:event_id>', methods=['POST'])
@login_required
def delete_event_route(event_id):
    event = Event.query.get(event_id)
    if event and event.owner_id == current_user.id:  # ensure the current user is the owner
        delete_event(event_id)
        return jsonify(success=True)
    return jsonify(success=False, message="Event not found or you don't have the permission to delete it")


@home.route('/users', methods=['GET'])
@login_required
def users_page():
    current_page = 'Users'
    all_users = userRepo.get_all_users()
    all_roles = userRepo.get_roles_values()
    return render_template('home/users.html', users=all_users, roles=all_roles, current_page=current_page)


@home.route('/change-role/<int:user_id>', methods=['POST'])
@login_required
def change_role(user_id):
    new_role = request.form.get('role')
    userRepo.change_user_role(user_id, new_role)
    return redirect(url_for('home.users_page'))


@home.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    userRepo.delete_user(user_id)
    return redirect(url_for('home.users_page'))
    

@home.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create_task_route():
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
        return redirect(url_for('home.tasks'))

    users = User.query.all()
    return render_template('home/create_task.html', users=users, current_page=current_page)


@home.route('/tasks', methods=['GET'])
@login_required
def tasks():
    current_page = 'Tasks'
    if current_user.role == UserRole.BASIC:
        # If the user is basic, show only tasks assigned to them
        tasks = taskRepo.get_tasks_by_user(current_user.id)
    else:
        # If the user has higher privileges, show all tasks
        tasks = taskRepo.get_all_tasks()

    return render_template('home/tasks.html', tasks=tasks, UserRole=UserRole, current_page=current_page)


@home.route('/tasks/edit/<int:task_id>/', methods=['GET', 'POST'])
@login_required
def edit_task_route(task_id):
    current_page = 'Tasks'
    # Check if the user has permission to edit tasks
    if current_user.role == UserRole.BASIC:
        flash('You do not have permission to edit tasks.')
        return redirect(url_for('home.tasks'))

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
        return redirect(url_for('home.tasks'))

    users = User.query.all()
    return render_template('home/edit_task.html', task=task, users=users, current_page=current_page)


@home.route('/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task_route(task_id):
    # Check if the user has permission to delete tasks
    if current_user.role == UserRole.BASIC:
        flash('You do not have permission to delete tasks.')
        return redirect(url_for('home.tasks'))

    try:
        taskRepo.delete_task(task_id)
        flash('Task deleted successfully.')
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('home.tasks'))


@home.route('/tasks/update_status/<int:task_id>', methods=['POST'])
@login_required
def update_task_status_route(task_id):
    if current_user.role != UserRole.BASIC:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('home.tasks'))

    new_status = request.form.get('status')

    try:
        task = taskRepo.get_task_by_id(task_id)
        if task:
            taskRepo.update_task_status(task_id, TaskStatus[new_status.upper()])
            flash('Task status updated successfully.')
    except ValueError as e:
        flash(str(e))

    return redirect(url_for('home.tasks'))


@home.app_template_filter('formatdatetime')
def format_datetime_filter(value, format="%a %b %-d, %-I%p"):
    if value is None:
        return ""
    # Ensure that the value is a datetime object
    if isinstance(value, str):
        value = datetime.fromisoformat(value)

    # Adjust the format string if you're using Windows, as it does not support '-' modifier
    if os.name == 'nt':
        format = format.replace('%-', '%#')

    return value.strftime(format)
