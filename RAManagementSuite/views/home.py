from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import login_required, current_user

from RAManagementSuite.models import Event
from RAManagementSuite.repos import announcementRepo
from RAManagementSuite.repos.eventRepo import create_event, get_all_events

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
        # get data from form and create an event
        title = request.form.get('title')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        owner_id = current_user.id
        color = request.form.get('color')
        create_event(title, start_date, end_date, owner_id, color)
        return redirect(url_for('home.events'))

    events = get_all_events()
    return render_template('home/events.html', events=events)

@login_required
@home.route('/api/events', methods=['GET'])
def get_events():
    # Fetch events from your database
    events = Event.query.all()
    events_data = [{
        'title': event.title,  # Combine event title with owner's name
        'start': event.start_date.isoformat(),
        'end': event.end_date.isoformat(),
        'color': event.color,
        'url': url_for('home.events')  # Pointing back to the main calendar
    } for event in events]

    return jsonify(events_data)