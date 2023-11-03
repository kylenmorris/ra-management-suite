from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user

from RAManagementSuite.repos import announcementRepo

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
