import os
from newsapi import NewsApiClient
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WORDS_PER_PAGE = 20
    YANDEX_DICTIONARY_KEY = os.environ.get('YANDEX_DICTIONARY_KEY') or 'dict.1.1.20200813T170611Z.344edb4fae05f097.9f74cfd69db39bcd1d50fccb83112af2ba5e6290'
    LANGUAGES = ['en','ru']
    NEWSAPI = NewsApiClient(api_key='3221932dd191465fa7332c86eb222a00')