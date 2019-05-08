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
    is_admin = db.BooleanField(default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class Training(db.Document):
    training_id = db.SequenceField(unique=True)
    title = db.StringField(max_length=100)
    description = db.StringField()
    location = db.StringField(max_length=255)
    datetime = db.DateTimeField()


class Enrollment(db.Document):
    user_id = db.IntField()
    training_id = db.IntField()
    evaluation_id = db.IntField()
    test_score = db.IntField()


class Evaluation(db.Document):
    evaluation_id = db.IntField(unique=True)
    opinion = db.StringField()
    is_trainer_good = db.BooleanField()
    criticism_suggestion = db.StringField()
    want_more = db.BooleanField()


class WikimediaProject(db.Document):
    wikimedia_project_id = db.IntField(unique=True)
    name = db.StringField()
    description = db.StringField()


class InterestedProject(db.Document):
    evaluation_id = db.IntField()
    wikimedia_project_id = db.IntField()



