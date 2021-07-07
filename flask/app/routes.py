from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
@app.route("/")
@app.route('/index')
def index():
    user = {'username':'Thomas'}
    posts = [
        {
            'author': {'username': 'John'},
            'body':'Dit is het bericht van John'
        },
        {
            'author': {'username':'Susan'},
            'body': 'Dit is het bericht van Susan.'
        }
    ]
    return render_template('index.html', user=user, posts=posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', form=form)
