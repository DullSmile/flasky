#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import render_template
from . import auth
from flask_login import login_required #8.2保护路由

@auth.route('/login')
def login():
    return render_template('auth/login.html')

#保护路由,只允许认证用户访问
@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'