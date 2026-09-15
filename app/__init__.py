from  flask import Flask
from config import Config
from .extensions import db,login
from .models import Enquiry,Shipment,User
from .main import bp
from .auth import auth_bp
import click
from werkzeug.security import generate_password_hash

import os
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        app.instance_path, "app.db"
    )
   
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # already exists — fine
    db.init_app(app)
    @app.cli.command("create-admin")
    def create_admin():
        username = click.prompt("Username")
        password = click.prompt(
            "Password",
            hide_input=True,
            confirmation_prompt=True
        )

        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        print(f"Admin user '{username}' created successfully.")
    login.init_app(app)
    login.login_view="auth.login"
    with app.app_context():
        db.create_all()

    app.register_blueprint(bp)     
    app.register_blueprint(auth_bp)

    return app
