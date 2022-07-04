from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "customers.db"


def make_app():
    app = Flask(__name__, static_folder='./static')
    app.config['SECRET_KEY'] = 'F0267sTRAWDLKJFYGKlknjh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}?check_same_thread=False'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    ########################################
    app.config['check_same_thread'] = False
    app.config['SQLALCHEMY_CHECK_SAME_THREAD'] = False
    ########################################
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .configuration import configuration
    from .assets import assets
    from .reports import reports
    from .base import base
    from .device_details import device_details

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(configuration, url_prefix='/')
    app.register_blueprint(assets, url_prefix='/')
    app.register_blueprint(reports, url_prefix='/')
    app.register_blueprint(base, url_prefix='/')
    app.register_blueprint(device_details, url_prefix='/')
    from .datamodels import User


    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('mainwebsite/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
