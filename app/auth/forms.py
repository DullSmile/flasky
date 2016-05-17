#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, PasswordField, ValidationError
from wtforms.validators import Required, DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class Login_Form(Form):
    email = StringField('Email:', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('password:', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email:', validators=[DataRequired(), Length(1, 64),
                                              Email()
                                              ]
                        )

    username = StringField('username:',
                           validators=[DataRequired(), Length(1, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have letters,'
                                              'nummbers, dots, or underscores'
                                              )
                                       ]
                           )

    password = PasswordField('password:', validators=[DataRequired(),
                                                      EqualTo('password2', message='Passwords must match.')
                                                      ]
                             )

    password2 = PasswordField('password:', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email exit.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            return ValidationError('username exit.')


# todo
class ChangePassWordForm(Form):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired()])
    password2 = PasswordField('Confirm New password', validators=[DataRequired()])
    submit = SubmitField('submit')

# todo
class ChangeEmailForm(Form):
    email =StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email has registered.')
