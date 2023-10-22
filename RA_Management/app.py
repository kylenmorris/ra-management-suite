from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_announcement(announcement_id):
    conn = get_db_connection()
    announcement = conn.execute('SELECT * FROM announcements WHERE id = ?',
                                (announcement_id,)).fetchone()
    conn.close()
    if announcement is None:
        abort(404)
    return announcement


@app.route('/')
def index():
    conn = get_db_connection()
    announcements = conn.execute('SELECT * FROM announcements').fetchall()
    conn.close()
    return render_template('index.html', announcements=announcements)


@app.route('/<int:announcement_id>')
def announcement(announcement_id):
    announcement = get_announcement(announcement_id)
    return render_template('announcement.html', announcement=announcement)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO announcements (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

