from flask import Flask, render_template, request, url_for, flash, redirect
from views.home import home

app = Flask(__name__)
app.register_blueprint(home)

if __name__ == '__main__':
    app.run()
