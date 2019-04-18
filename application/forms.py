from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User


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
                      choices=[('', 'Pekerjaan'), ('Pegawai Negeri Sipil', 'Pegawai Negeri Sipil'), ('Pegawai Swasta', 'Pegawai Swasta'),
                               ('Wirausaha', 'Wirausaha'), ('Pelajar', 'Pelajar'), ('Lain-lain', 'Lain-lain')])
    city = StringField('Kota', validators=[DataRequired()])
    submit = SubmitField("Daftar")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError('Alamat email sudah digunakan. Silakan gunakan alamat lain')
