from  flask import Flask
from config import Config
from .extensions import db
from .models import Enquiry,Shipment
from .main import bp
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
    with app.app_context():
        db.create_all()

    app.register_blueprint(bp)

    return app
