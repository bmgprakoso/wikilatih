from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, RadioField, \
    SelectMultipleField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from application.models import User
from city import city


class LoginForm(FlaskForm):
    email = StringField("Alamat Email", validators=[DataRequired(), Email()])
    password = PasswordField("Kata Sandi", validators=[DataRequired(), Length(min=6, max=15)])
    remember_me = BooleanField("Ingat Saya")
    submit = SubmitField("Masuk")


class RegisterForm(FlaskForm):
    name = StringField("Nama Lengkap", validators=[DataRequired(), Length(min=2, max=55)])
    email = StringField("Alamat Email", validators=[DataRequired(), Email()])
    password = PasswordField("Kata Sandi", validators=[DataRequired(), Length(min=6, max=15)])
    password_confirm = PasswordField("Ulang Kata Sandi",
                                     validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])
    phone = StringField("Nomor Telepon", validators=[DataRequired(), Length(min=2, max=15)])
    job = SelectField('Pekerjaan', validators=[DataRequired()],
                      choices=[('', 'Pekerjaan'), ('Pegawai Negeri Sipil', 'Pegawai Negeri Sipil'),
                               ('Pegawai Swasta', 'Pegawai Swasta'),
                               ('Wirausaha', 'Wirausaha'), ('Pelajar', 'Pelajar'), ('Lain-lain', 'Lain-lain')])
    city = SelectField('Kota', validators=[DataRequired()],
                       choices=city)
    submit = SubmitField("Daftar")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError('Alamat email sudah digunakan. Silakan gunakan alamat lain')


class TrainingForm(FlaskForm):
    title = StringField('Nama Pelatihan', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Deskripsi', validators=[DataRequired(), Length(min=2, max=255)])
    location = StringField('Lokasi', validators=[DataRequired(), Length(min=2, max=255)])
    date = DateField('Tanggal Pelatihan', validators=[DataRequired()])
    time = TimeField('Waktu Pelatihan', validators=[DataRequired()])
    submit = SubmitField("Kirim")


class TestForm(FlaskForm):
    question1 = RadioField('Question 1',
                           choices=[('A', 'Answer A'), ('B', 'Answer B'), ('C', 'Answer C'), ('D', 'Answer D')],
                           validators=[DataRequired()])
    question2 = RadioField('Question 2',
                           choices=[('A', 'Answer A'), ('B', 'Answer B'), ('C', 'Answer C'), ('D', 'Answer D')],
                           validators=[DataRequired()])
    question3 = RadioField('Question 3',
                           choices=[('A', 'Answer A'), ('B', 'Answer B'), ('C', 'Answer C'), ('D', 'Answer D')],
                           validators=[DataRequired()])
    question4 = RadioField('Question 4',
                           choices=[('A', 'Answer A'), ('B', 'Answer B'), ('C', 'Answer C'), ('D', 'Answer D')],
                           validators=[DataRequired()])
    question5 = RadioField('Question 5',
                           choices=[('A', 'Answer A'), ('B', 'Answer B'), ('C', 'Answer C'), ('D', 'Answer D')],
                           validators=[DataRequired()])
    submit = SubmitField('Kirim')


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class EvaluationForm(FlaskForm):
    opinion = TextAreaField('Apa pendapat Anda terkait pelatihan yang telah diikuti?*', validators=[DataRequired()])
    is_trainer_good = RadioField('Apakah pelatih memberikan penjelasan dengan baik dan mudah dimengerti?*',
                                 choices=[(True, 'Ya'), (False, 'Tidak')],
                                 validators=[DataRequired()])
    interested_wikimedia_project = MultiCheckboxField(
        'Selain Wikipedia, proyek Wikimedia mana saja yang tertarik untuk Anda ikuti?*',
        validators=[DataRequired()],
        choices=[('wiktionary', 'Wiktionary (kamus)'), ('wikisource', 'Wikisource (sumber naskah, buku)'),
                 ('wikiquote', 'Wikiquote (kutipan)'), ('wikibooks', 'Wikibooks (buku)'),
                 ('wikinews', 'Wikinews (berita)'), ('wikiversity', 'Wikiversity (bahan pelajaran)'),
                 ('wikispecies', 'Wikispecies (taksonomi)'), ('mediawiki', 'MediaWiki (piranti lunak)'),
                 ('wikidata', 'Wikidata (basis data)'),
                 ('wikimedia_commons', 'Wikimedia Commons (gudang berkas: foto, video, musik)'),
                 ('wikivoyage', 'Wikivoyage (panduan wisata)')])
    criticism_suggestion = TextAreaField('Kritik dan saran*', validators=[DataRequired()])
    want_more = BooleanField('Saya berminat untuk mengikuti pelatihan selanjutnya',
                             validators=[DataRequired()])
    submit = SubmitField("Kirim")
