import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cb6f2902-fce9-41c5-bb03-29f4b0f2b9c6'
    MONGODB_SETTINGS = {
        'db': 'wikilatih',
        'host': 'mongodb+srv://wikilatih:wikilatih1234@cluster0-hotgr.mongodb.net/wikilatih?retryWrites=true&ssl=true',
        'connect': False
    }
    # MONGODB_SETTINGS = {
    #     'db': 'wikilatih'
    # }
