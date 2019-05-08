from application import app, mail
from flask_mail import Message
from flask import render_template


def send_enrollment_info(email, training_name):
    try:
        msg = Message(f'Pendaftaran Pelatihan {training_name}', sender='wikilatih.app@gmail.com',
                      recipients=[email])
        msg.body = f'Anda sudah terdaftar di pelatihan {training_name} melalui website WikiLatih.' \
                   'Silakan gunakan kode QR dibawah untuk mengisi presensi di acara nanti. Terima kasih.'

        msg.html = render_template('enrollment-mail.html', training_name=training_name)

        mail.send(msg)
        return True
    except:
        return False


def send_attendance_certificate(email):
    try:
        msg = Message('Sertifikat Kehadiran dari WikiLatih', sender='wikilatih.app@gmail.com',
                      recipients=[email])
        msg.body = "Selamat atas kehadiran Anda di kegiatan pelatihan WikiLatih. " \
                   "Berikut dilampirkan dokumen sertifikat kehadiran. Terima kasih."

        with app.open_resource("static/pdf/certificate_of_attendance.pdf") as fp:
            msg.attach("certificate_of_attendance.pdf", "application/pdf", fp.read())

        mail.send(msg)
        return True
    except:
        return False


def send_qualification_certificate(email):
    try:
        print(email)
        msg = Message('Sertifikat Kualifikasi dari WikiLatih', sender='wikilatih.app@gmail.com',
                      recipients=[email])
        msg.body = "Selamat, Anda telah lulus uji kompetensi kegiatan pelatihan WikiLatih. " \
                   "Berikut dilampirkan dokumen sertifikat kualifikasi. Terima kasih."

        with app.open_resource("static/pdf/certificate_of_qualification.pdf") as fp:
            msg.attach("certificate_of_qualification.pdf", "application/pdf", fp.read())

        mail.send(msg)
        return True
    except:
        return False
