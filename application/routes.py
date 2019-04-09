from application import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html',)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/trainings')
def trainings():
    return render_template('trainings.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


