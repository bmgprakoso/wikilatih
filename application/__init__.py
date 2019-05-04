from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_bower import Bower

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)
Bower(app)

from application import routes
