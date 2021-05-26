from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import os


bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)


    #attach routes and custom pages
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .portal import portal as portal_blueprint

    app.register_blueprint(portal_blueprint, url_prefix='/portal')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
    return app
