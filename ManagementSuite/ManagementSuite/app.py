import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('C:\\D Drive\\school\\CMPT-370\\gitlab\\ManagementSuite\\ManagementSuite\\db\\schema.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    announcements = conn.execute('SELECT * FROM Announcements').fetchall()
    conn.close()
    return render_template('templates\\home\\index.html', announcements = announcements)


if __name__ == "__main__":
    app.run()

