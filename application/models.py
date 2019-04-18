from application import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document):
    user_id = db.IntField(unique=True)
    name = db.StringField(max_length=100)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()
    phone = db.StringField()
    job = db.StringField()
    city = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class Training(db.Document):
    course_id = db.IntField(unique=True)
    title = db.StringField(max_length=100)
    description = db.StringField(max_length=255)
    location = db.StringField(max_length=255)
    date = db.DateTimeField()


class Enrollment(db.Document):
    user_id = db.IntField()
    course_id = db.IntField()
