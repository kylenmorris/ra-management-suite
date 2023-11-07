from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import login_required, current_user

from RAManagementSuite.models import Event, UserRole, TaskPriority, User, TaskStatus
from RAManagementSuite.repos import announcementRepo, taskRepo
from RAManagementSuite.repos.eventRepo import create_event, get_all_events, update_event, delete_event
#from RAManagementSuite.repos.taskRepo import create_task, get_all_tasks, get_task_by_id, update_task

home = Blueprint('home', __name__)


@home.route('/')
def index():
    announcements = announcementRepo.get_announcements()
    return render_template('home/index.html', announcements=announcements)


@home.route('/view/<int:announcement_id>')
def announcement(announcement_id):
    announcement = announcementRepo.get_announcement(announcement_id)
    return render_template('home/view.html', announcement=announcement)


@home.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            announcementRepo.create_announcement(title, content)
            return redirect(url_for('home.index'))

    return render_template('home/create.html')


@home.route('/edit/<int:announcement_id>/', methods=('GET', 'POST'))
def edit(announcement_id):
    announcement = announcementRepo.get_announcement(announcement_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            announcementRepo.edit_announcement(title, content, announcement_id)
            return redirect(url_for('home.index'))

    return render_template('home/edit.html', announcement=announcement)


@home.route('/profile')
@login_required
def profile():
    return render_template('home/profile.html', name=current_user.name)


@home.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    if request.method == 'POST':
        # get data from form and create or update an event
        title = request.form.get('title')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        owner_id = current_user.id
        color = request.form.get('color')
        description = request.form.get('description')
        event_id = request.form.get('event_id')

        if event_id and event_id.strip() != '':  # If event_id is provided, it's an update
            update_event(event_id, title, start_date, end_date, color, description)
        else:  # Otherwise, it's a new event
            create_event(title, start_date, end_date, owner_id, color, description)
        return redirect(url_for('home.events'))

    events = get_all_events()
    return render_template('home/events.html', events=events, current_user=current_user)


@login_required
@home.route('/api/events', methods=['GET'])
def get_events():
    # Fetch events from your database
    events = Event.query.all()
    events_data = [{
        'id': event.id,
        'title': event.title,  # Combine event title with owner's name
        'start': event.start_date.isoformat(),
        'end': event.end_date.isoformat(),
        'color': event.color,
        'description': event.description,
        # 'url': url_for('home.events'),  # Pointing back to the main calendar
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


@home.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create_task_route():
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
    return render_template('home/create_task.html', users=users)


@home.route('/tasks', methods=['GET'])
@login_required
def tasks():
    if current_user.role == UserRole.BASIC:
        # If the user is basic, show only tasks assigned to them
        tasks = taskRepo.get_tasks_by_user(current_user.id)
    else:
        # If the user has higher privileges, show all tasks
        tasks = taskRepo.get_all_tasks()

    return render_template('home/tasks.html', tasks=tasks)


@home.route('/tasks/edit/<int:task_id>/', methods=['GET', 'POST'])
@login_required
def edit_task_route(task_id):
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
    return render_template('home/edit_task.html', task=task, users=users)


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



