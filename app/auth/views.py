#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import render_template, redirect, request, flash, url_for
from flask_login import login_user,login_required, logout_user
from flask_login import login_required #8.2保护路由
from . import auth
from app import db
from ..models import User
from .forms import Login_Form, RegistrationForm

#保护路由,只允许认证用户访问
@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalidd username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data
                    )
        db.session.add(user)
        flash('regist sucessful!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)