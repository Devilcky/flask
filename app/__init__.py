'''
    创建应用程序，并注册相关蓝图
'''
from flask import Flask
# from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
from app.models.base import db
from app.libs.email import mail
from flask_cache import Cache
from app.libs.limiter import Limiter

__author__ = '七月'

login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'simple'})
limiter = Limiter()


def register_web_blueprint(app):
    from app.web import web
    app.register_blueprint(web)


# def register_api_blueprint(app):
#     from app.api import account
#     app.register_blueprint(account.app,url_prefix='/api')


def create_app(config=None):
    app = Flask(__name__)

    #: load default configuration
    app.config.from_object('app.settings')
    app.config.from_object('app.secure')

    # 注册SQLAlchemy
    db.init_app(app)

    # 注册email模块
    mail.init_app(app)

    # 注册login模块
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    # 注册flask-cache模块
    cache.init_app(app)

    # 注册CSRF保护
    # csrf = CsrfProtect()
    # csrf.init_app(app)

    # register_api_blueprint(app)
    register_web_blueprint(app)

    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    return app
