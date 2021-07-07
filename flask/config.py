import os
basedir = os.path.abspath(os.path.dirname('fleur home huiswerk assistent.py'))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'fleur_home_huiswerk_assistent.db')
