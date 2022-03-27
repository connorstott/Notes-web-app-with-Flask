from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def createApp() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'apwof8yaeoifuwe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    createDb(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def createDb(app: Flask) -> None:
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")