from application import app
from application.models import User, Training
from flask import render_template, redirect, flash, session
from application.forms import LoginForm, RegisterForm


@app.route('/')
def index():
    logged_name = ''
    if session.get('user_id'):
        logged_name = session.get('name')

    trainings = Training.objects.all()
    return render_template('index.html', trainings=trainings, logged_name=logged_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f'{user.name}, kamu berhasil masuk', 'success')
            session['user_id'] = user.user_id
            session['name'] = user.name
            return redirect('/')
        else:
            flash('Mohon maaf, sedang ada gangguan sistem. Silakan kembali beberapa saat lagi', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect('/')

    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1

        name = form.name.data
        email = form.email.data
        password = form.password.data
        phone = form.phone.data
        job = form.job.data
        city = form.city.data

        user = User(user_id=user_id, name=name, email=email, phone=phone, job=job, city=city)
        user.set_password(password)
        user.save()
        flash('Kamu berhasil terdaftar', 'success')
        return redirect('/')

    return render_template('register.html', form=form)


@app.route('/account')
def account():
    logged_in = False
    if session.get('user_id'):
        logged_in = True

    return render_template('account.html', logged_in=logged_in)
