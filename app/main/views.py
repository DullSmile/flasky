# -*-coding:utf-8-*-
from flask import render_template, abort, redirect, session, url_for
from datetime import datetime
from . import main
from ..models import User
from forms import NameForm

@main.route('/')
def index():
    #return render_template('index.html')
    form = NameForm()
    if form.validate_on_submit():
        #...
        return redirect(url_for('index'))
    return render_template('index.html',
                           form = form,
                           name = session.get('name'),
                           known = session.get('known', False),
                           current_time = datetime.utcnow())


#用户资料页面路由
@main.route('/user/<username>')
def user(username):
    print(username)
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
