from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, login
from app.forms import LoginForm, EditProfileForm, FleurhomeForm
from app.models import User
from app.error import Auth403Error
from config import Config
from lib import fleurhome

@app.before_request
def before_request():
    if not current_user.is_anonymous:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=["GET", "POST"])
@login_required
def index():
    form = FleurhomeForm(request.form)
    print(form.validate())
    if request.method == 'POST':
        fleurhome.webrun(form.vak, form.dag)
    return render_template('index.html', title='index', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/admin/')
@login_required
def admin():
    inconfig = current_user.username in app.config['ADMINS']
    if inconfig:
        return render_template('admin.html', user=current_user, inconfig=inconfig)
    else:
        return render_template('403.html'), 403

@app.errorhandler(403)
def _403(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def _404(error):
    return render_template('404.html'), 404
