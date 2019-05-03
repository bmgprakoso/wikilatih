from application import app
from application.models import User, Training
from flask import render_template, redirect, flash, session
from application.forms import LoginForm, RegisterForm, TestForm, EvaluationForm, TrainingForm
import datetime


def get_context():
    context = dict()
    context['logged_in'] = session.get('user_id', None)
    context['logged_name'] = session.get('name', '')
    context['is_admin'] = session.get('is_admin', False)

    return context


@app.route('/')
def index():
    context = get_context()
    t = Training.objects.all()
    return render_template('index.html', trainings=t, context=context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    context = get_context()
    if context['logged_in']:
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
            session['is_admin'] = user.is_admin
            return redirect('/')
        else:
            flash('Mohon maaf, sedang ada gangguan sistem. Silakan kembali beberapa saat lagi', 'danger')
    return render_template('login.html', form=form, context=context)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('is_admin', None)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    context = get_context()
    if context['logged_in']:
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

    return render_template('register.html', form=form, context=context)


@app.route('/account')
def account():
    context = get_context()
    if not context['logged_in']:
        return redirect('/')

    return render_template('account.html', context=context)


@app.route('/trainings/<training_id>')
def trainings(training_id):
    context = get_context()
    if not context['logged_in']:
        return redirect('/')

    return render_template('training-detail.html', context=context)


@app.route('/trainings/<training_id>/test', methods=['GET', 'POST'])
def test(training_id):
    context = get_context()
    if not context['logged_in']:
        return redirect('/')

    t = Training.objects.all()

    form = TestForm()
    if form.validate_on_submit():
        flash('Jawaban berhasil disimpan', 'success')
        return redirect('/')

    return render_template('test.html', training=t, form=form, context=context)


@app.route('/trainings/<training_id>/evaluation', methods=['GET', 'POST'])
def evaluation(training_id):
    context = get_context()
    if not context['logged_in']:
        return redirect('/')

    t = Training.objects.all()

    form = EvaluationForm()
    if form.validate_on_submit():
        flash('Terima kasih atas ulasanmu', 'success')
        return redirect('/')

    return render_template('evaluation.html', training=t, form=form, context=context)


@app.route('/admin/trainings')
def admin_training_list():
    context = get_context()
    if not context['logged_in']:
        return redirect('/')

    t = Training.objects.all()
    return render_template('admin/training-list.html', trainings=t, context=context)


@app.route('/admin/trainings/new', methods=['GET', 'POST'])
def admin_training_new():
    context = get_context()
    if not context['logged_in']:
        return redirect('/')

    form = TrainingForm()
    if form.validate_on_submit():
        training_id = Training.objects.count()
        training_id += 1

        title = form.title.data
        description = form.description.data
        location = form.location.data
        date = form.date.data
        time = form.time.data

        date_time = datetime.datetime.combine(date, time)

        training = Training(training_id=training_id, title=title, description=description, location=location,
                            datetime=date_time)
        training.save()
        flash('Pelatihan berhasil terdaftar', 'success')
        return redirect('/admin/trainings')

    return render_template('admin/training-form.html', context=context, form=form)


@app.route('/admin/trainings/<training_id>/edit', methods=['GET', 'POST'])
def admin_training_edit(training_id):
    context = get_context()
    if not context['logged_in']:
        return redirect('/')

    t = Training.objects.get(training_id=training_id)

    form = TrainingForm(obj=t)
    form.date.data = t.datetime.date()
    form.time.data = t.datetime.time()

    if form.validate_on_submit():
        t.title = form.title.data
        t.description = form.description.data
        t.location = form.location.data
        t.datetime = datetime.datetime.combine(form.date.data, form.time.data)
        t.save()
        flash('Pelatihan berhasil diubah', 'success')
        return redirect('/admin/trainings')

    return render_template('admin/training-form.html', context=context, form=form)


@app.route('/admin/trainings/<training_id>/delete', methods=['GET', 'POST'])
def admin_training_delete(training_id):
    context = get_context()
    if not context['logged_in']:
        return redirect('/')

    t = Training.objects.get(training_id=training_id)
    t.delete()

    return redirect('/admin/trainings')
