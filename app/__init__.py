# -*-coding:utf-8-*-
"""程序的工厂函数在app包中的构造文件定义"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
from flask_login import LoginManager




bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

#实例化login_manager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # ?init_app()函数
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    # 在工厂函数中初始化认证用户
    login_manager.init_app(app)
    #print(login_manager)
    # 附加路由和自定义的错误页面

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)
    #print(main_blueprint)

    #将auth认证蓝本注册到create_app函数中
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    # 加载用户的回调函数LoginManager.user_loader
    @login_manager.user_loader
    def load_user(user_id):
        print("加载用户回调函数load_user from app.init模块")
        from app.models import User
        return User.query.get(int(user_id))

    return app