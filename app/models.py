#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash #密码散列
from flask_login import UserMixin #认证用户
from . import login_manager #加载用户的回调函数
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #确认用户账户

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' %self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': (
                Permission.FOLLOW |
                Permission.COMMENT |
                Permission.WRITE_ARTICLES,
                True
                     ),
            'Moderator': (
                Permission.FOLLOW |
                Permission.COMMENT |
                Permission.WRITE_ARTICLES |
                Permission.MODERATE_COMMENTS,
                False
                     ),
            'Administrator': (
                0xff,
                False
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
           # print("role: ", role)
           # print("r: ", r)
            if role is None:
                role = Role(name=r)
                print(role)
                print (roles[r])
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
        db.session.commit()


#Role权限代码
class Permission:
    FOLLOW = 0x01
    COMMENT = 0X02
    WRITE_ARTICLES = 0X04
    MODERATE_COMMENTS = 0X08
    ADMINISTER = 0X80


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return '<User %r>' %self.username

    @property
    def password(self):
        raise AttributeError('password is note a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #加载用户的回调函数
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #生成令牌,有效期为1小时
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    #检验令牌
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True