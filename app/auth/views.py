#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from app import db
from ..models import User
from ..email import send_email, close_thr
from .forms import Login_Form, RegistrationForm, ChangePassWordForm,ChangeEmailForm


#
@auth.before_app_request
def before_request():
    if not current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint[:5] != 'auth.'\
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


#登陆路由
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            #user.confirmed=True
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalidd username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    #print(current_user.confirmed)
    #current_user.confirmed = False
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
        db.session.commit()
        token = user.generate_confirmation_token()
        thr = send_email(user.email,'Confirm Your Account', 'auth/email/confirm', token=token, user=user)
        close_thr(thr)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('mail.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               'Confirm you accout',
               'auth/email/confirm',
               user=current_user,
               token=token
               )
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

#修改密码
@auth.route('/change-password', methods=[' GET', 'POSR'])
@login_required
def change_password():
    form = ChangePassWordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been undated.')
            logout()
            #return url_for('main.index')
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)

# 修改邮箱
@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email.change_token(new_email)
            send_email(new_email, 'Confirm your email address.', 'auth/email/change_email', user=current_user, token=token)
            flash('an email with instructions to confirm your email address has been sent to you')
            return render_template('auth/change_email.html', form=form)
        else:
            flash('Invalid email or password.')
    return render_template('auth/change_email.html', form=form)

