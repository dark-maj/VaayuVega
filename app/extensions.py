from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme

db=SQLAlchemy()
login=LoginManager()
admin=Admin(name="Vaayu Vega Admin", theme=Bootstrap4Theme())
