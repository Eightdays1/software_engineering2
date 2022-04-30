from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from website.config import BaseConfig


db = SQLAlchemy()
app = Flask(__name__)


def create_app(base_config=BaseConfig):
    app.config.from_object(base_config)

    db.init_app(app)

    from .models import User, Group

    if not path.exists('website/' + base_config.DB_NAME):
        db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
