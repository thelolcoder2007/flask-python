import os
basedir = os.path.abspath(os.path.dirname('fleur home huiswerk assistent.py'))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-terents-alpha0.0.1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'fleur_home_huiswerk_assistent.db')
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'simon.vanharingen@gmail.com'
    MAIL_PASSWORD = 'mvpysbabzlsgkmyt'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    ADMINS = ['thomas.erents@gmail.com']
    
