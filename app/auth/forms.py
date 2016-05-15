#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Required, DataRequired, Length, Email

class Login_Form(Form):
    email = StringField('Email:', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('password:', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')