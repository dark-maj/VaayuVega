from  flask import Flask
from config import Config
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

    @app.route("/")
    def hello_world():
        return "<p>Hello World</p>"

    return app
