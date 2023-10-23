from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect
from repos import announcementRepo

home = Blueprint('home', __name__)


@home.route('/')
def index():
    announcements = announcementRepo.get_announcements()
    return render_template('home/index.html', announcements=announcements)


@home.route('/<int:announcement_id>')
def announcement(announcement_id):
    announcement = announcementRepo.get_announcement(announcement_id)
    return render_template('home/announcement.html', announcement=announcement)


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


@home.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    announcement = announcementRepo.get_announcement(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            announcementRepo.edit_announcement(title, content, id)
            return redirect(url_for('home.index'))

    return render_template('home/edit.html', announcement=announcement)









