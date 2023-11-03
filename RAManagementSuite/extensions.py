from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# this file is just to prevent a circular wait between
# models and __init__.py
db = SQLAlchemy()
migrate = Migrate()
