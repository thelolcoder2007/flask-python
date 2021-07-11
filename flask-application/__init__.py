from flask import Flask, render_template, request, flash, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/data/', methods=['GET', 'POST'])
def data():
    global form_data
    if request.method == 'GET':
        flash('The URL /data is accessed directly. Go to / instead')
        return redirect(url_for(index))
    elif request.method == 'POST':
        form_data = request.form
        return render_template('data.html', form_data=form_data)

import fleurhome
app.run(host='10.0.111.128', port=80)
