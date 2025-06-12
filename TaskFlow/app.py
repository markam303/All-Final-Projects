"""
TaskFlow application:
Manage your everyday tasks in convenient way.
Main application logic.
"""

from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User
from auth import auth as auth_blueprint
from tasks import tasks as tasks_blueprint
from database import init_database


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "1"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskflow.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    init_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: int) -> User | None:
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        return render_template("index.html")

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(tasks_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
