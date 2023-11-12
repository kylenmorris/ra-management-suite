from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import login_required, current_user

from models import Event
from repos import announcementRepo
from repos.eventRepo import create_event, get_all_events, update_event, delete_event
from repos import userRepo

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
    return render_template('home/announcement.html', announcements=announcements, current_page=current_page)

@home.route('/view/<int:announcement_id>')
def announcement(announcement_id):
    announcement = announcementRepo.get_announcement(announcement_id)
    return render_template('home/view.html', announcement=announcement)


@home.route('/create', methods=('GET', 'POST'))
def create():
    current_page = 'new_announcement'
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            announcementRepo.create_announcement(title, content)
            return redirect(url_for('home.announcement_page'))

    return render_template('home/create.html', current_page=current_page)


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
            return redirect(url_for('home.announcement_page'))

    return render_template('home/edit.html', announcement=announcement)


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
    return render_template('home/events.html', events=events, current_user=current_user, current_page=current_page)


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





