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

event = Blueprint('event', __name__)


@event.route('/', methods=['GET', 'POST'])
@login_required
def index():
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
        return redirect(url_for('event.index'))

    events = get_all_events()
    users = User.query.all()
    # Filter events by type if a toggle is set, this should correspond to a filter in your frontend
    filter_type = request.args.get('type')
    if filter_type:
        events = [event for event in events if event.event_type == filter_type]

    return render_template('event/index.html', events=events, current_user=current_user,
                           EventType=EventType, UserRole=UserRole, users=users, current_page=current_page)


@event.route('/api/events', methods=['GET'])
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


@event.route('/delete/<int:event_id>', methods=['POST'])
@login_required
def delete(event_id):
    event = Event.query.get(event_id)
    if event and event.owner_id == current_user.id:  # ensure the current user is the owner
        delete_event(event_id)
        return jsonify(success=True)
    return jsonify(success=False, message="Event not found or you don't have the permission to delete it")


@event.app_template_filter('formatdatetime')
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