from application import app
from application.models import User, Training, Enrollment, Evaluation, InterestedProject
from flask import render_template, redirect, flash, session, url_for, Response
from application.forms import LoginForm, RegisterForm, TestForm, EvaluationForm, TrainingForm
from application.services import mail
import datetime
import random


def get_context():
    context = dict()
    context['user_id'] = session.get('user_id', None)
    context['email'] = session.get('email', None)
    context['logged_name'] = session.get('name', '')
    context['is_admin'] = session.get('is_admin', False)

    return context


@app.route('/')
def index():
    context = get_context()
    t = Training.objects.all()
    context['trainings'] = t

    if context['is_admin']:
        return render_template('dashboard.html', context=context)

    return render_template('index.html', context=context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    context = get_context()
    if context['user_id']:
        return redirect('/')

    form = LoginForm()
    context['form'] = form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f'{user.name}, kamu berhasil masuk.', 'success')
            session['user_id'] = user.user_id
            session['email'] = user.email
            session['name'] = user.name
            session['is_admin'] = user.is_admin
            return redirect('/')
        else:
            flash('Kata sandi salah atau akun belum terdaftar', 'danger')
    return render_template('login.html', context=context)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('name', None)
    session.pop('is_admin', None)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    context = get_context()
    if context['user_id']:
        return redirect('/')

    form = RegisterForm()
    context['form'] = form
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

    return render_template('register.html', context=context)


@app.route('/account')
def account():
    context = get_context()
    if not context['user_id']:
        return redirect('/')

    user = User.objects.get(user_id=context['user_id'])
    context['user'] = user

    enroll_list = Enrollment.objects.aggregate(*[
        {
            '$lookup': {
                'from': 'training',
                'localField': 'training_id',
                'foreignField': 'training_id',
                'as': 'training_detail'
            }
        }, {
            '$match': {
                'user_id': context['user_id']
            }
        }
    ])
    context['enroll_list'] = list(enroll_list)

    return render_template('account.html', context=context)


@app.route('/trainings/<training_id>')
def training_detail(training_id):
    context = get_context()

    training = Training.objects.get(training_id=training_id)
    context['training'] = training

    if context['is_admin']:
        return render_template('admin-training-detail.html', context=context)

    try:
        enrollment = Enrollment.objects.get(user_id=context['user_id'], training_id=training_id)
        context['enrollment'] = enrollment
    except:
        context['enrollment'] = None

    return render_template('training-detail.html', context=context)


@app.route('/trainings/<training_id>/enroll')
def training_enrollment(training_id):
    context = get_context()
    if not context['user_id']:
        return redirect(url_for('register'))

    training = Training.objects.get(training_id=training_id)

    if training:
        if Enrollment.objects(user_id=context['user_id'], training_id=training_id):
            flash(f"Ups! Kamu telah terdaftar di pelatihan {training.title}!", "danger")
        else:
            Enrollment(user_id=session.get('user_id'), training_id=training_id).save()

            mail.send_enrollment_info(context['email'], training.title)

            flash(f"Kamu berhasil terdaftar di pelatihan {training.title}!", "success")

    return redirect(url_for('training_detail', training_id=training_id))


@app.route('/trainings/<training_id>/test', methods=['GET', 'POST'])
def test(training_id):
    context = get_context()
    if not context['user_id']:
        return redirect('/')

    training = Training.objects.get(training_id=training_id)
    if not training:
        return redirect('/')
    context['training'] = training

    try:
        enrollment = Enrollment.objects.get(user_id=context['user_id'], training_id=training_id)
    except:
        flash(f"Ups! Kamu belum terdaftar di pelatihan {training.title}!", "danger")
        return redirect(url_for('training_detail', training_id=training_id))

    form = TestForm()
    context['form'] = form

    if form.validate_on_submit():
        enrollment.test_score = random.randrange(75, 100)
        enrollment.save()

        mail.send_qualification_certificate(context['email'])

        flash('Jawaban berhasil disimpan', 'success')
        return redirect(url_for('training_detail', training_id=training_id))

    return render_template('test.html', context=context)


@app.route('/trainings/<training_id>/evaluation', methods=['GET', 'POST'])
def evaluation(training_id):
    context = get_context()
    if not context['user_id']:
        return redirect('/')

    training = Training.objects.get(training_id=training_id)
    if not training:
        return redirect('/')
    context['training'] = training

    try:
        enrollment = Enrollment.objects.get(user_id=context['user_id'], training_id=training_id)
    except:
        flash(f"Ups! Kamu belum terdaftar di pelatihan {training.title}!", "danger")
        return redirect(url_for('training_detail', training_id=training_id))

    form = EvaluationForm()
    context['form'] = form

    if form.validate_on_submit():
        evaluation_id = Evaluation.objects.count()
        evaluation_id += 1

        opinion = form.opinion.data
        is_trainer_good = form.is_trainer_good.data
        criticism_suggestion = form.criticism_suggestion.data
        want_more = form.want_more.data
        interested_projects = form.interested_wikimedia_project.data

        Evaluation(evaluation_id=evaluation_id, opinion=opinion, is_trainer_good=is_trainer_good,
                   criticism_suggestion=criticism_suggestion,
                   want_more=want_more).save()

        for ip in interested_projects:
            InterestedProject(evaluation_id=evaluation_id, wikimedia_project_id=int(ip)).save()

        enrollment.evaluation_id = evaluation_id
        enrollment.save()

        mail.send_attendance_certificate(context['email'])

        flash('Terima kasih atas ulasanmu', 'success')
        return redirect('/')

    return render_template('evaluation.html', context=context)


@app.route('/admin/trainings')
def admin_training_list():
    context = get_context()
    if not context['user_id']:
        return redirect('/')

    t = Training.objects.all()
    return render_template('admin/training-list.html', trainings=t, context=context)


@app.route('/admin/trainings/new', methods=['GET', 'POST'])
def admin_training_new():
    context = get_context()
    if not context['user_id']:
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
    if not context['user_id']:
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
    if not context['user_id']:
        return redirect('/')

    t = Training.objects.get(training_id=training_id)
    t.delete()

    return redirect('/admin/trainings')


@app.route("/download")
def download():
    content = 'ini adalah contoh hasil unduhan'
    return Response(content, mimetype="text/plain",
                    headers={"Content-disposition": "attachment; filename=download.txt"})
