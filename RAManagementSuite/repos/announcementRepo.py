import sqlite3
from RAManagementSuite.repos.baseRepo import get_db_connection
from werkzeug.exceptions import abort


def get_announcement(announcement_id):
    """
    Gets a single announcement by id.
    Aborts if no announcement is found.
    :param announcement_id: Announcement id
    :return: Single announcement
    """
    conn = get_db_connection()
    announcement = conn.execute('SELECT * FROM announcements WHERE id = ?',
                                (announcement_id,)).fetchone()
    conn.close()
    if announcement is None:
        abort(404)
    return announcement


def get_announcements():
    """
    Gets all existing announcements.
    :return: list of announcements
    """
    conn = get_db_connection()
    announcements = conn.execute('SELECT * FROM announcements').fetchall()
    conn.close()

    return announcements


def create_announcement(title, content):
    """
    Creates a new announcement.
    :param title: announcement title (string)
    :param content: announcement content (string)
    :return: none
    """
    conn = get_db_connection()
    conn.execute('INSERT INTO announcements (title, content) VALUES (?, ?)',
                 (title, content))
    conn.commit()
    conn.close()


def edit_announcement(title, content, id):
    """
    Edits an existing announcement.
    No error handling if announcement does not exist.
    :param title: announcement title (string)
    :param content: announcement content (string)
    :return: none
    """
    conn = get_db_connection()
    conn.execute('UPDATE announcements SET title = ?, content = ?'
                 ' WHERE id = ?',
                 (title, content, id))
    conn.commit()
    conn.close()

