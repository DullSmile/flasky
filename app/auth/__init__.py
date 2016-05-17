#!/usr/bin/env python
# -*-coding:utf-8-*-
from flask import Blueprint, url_for, request, redirect
from flask_login import current_user

auth = Blueprint('auth', __name__)

from . import views




