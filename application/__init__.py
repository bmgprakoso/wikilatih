from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

mail = Mail(app)

from application import routes
