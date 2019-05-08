import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cb6f2902-fce9-41c5-bb03-29f4b0f2b9c6'
    MONGODB_SETTINGS = {
        'db': 'wikilatih',
        'host': 'mongodb+srv://cluster0-hotgr.mongodb.net/wikilatih?retryWrites=true&ssl=true',
        'username': os.environ['DB_USER'],
        'password': os.environ['DB_PASSWORD'],
        'connect': False
    }
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ['EMAIL_USER']
    MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
