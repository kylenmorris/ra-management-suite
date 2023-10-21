from main import bp
import sqlite3
from flask import Flask, render_template

app = Flask(__name__,
            template_folder='C:\\D Drive\\school\\CMPT-370\\gitlab\\src\\src\\main\\templates')


def get_db_connection():
    conn = sqlite3.connect('src/src/db/schema.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


@bp.route('/')
def index():
    return 'This is The Main Blueprint'


if __name__ == "__main__":
    app.run()
