import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Dit-Is-Het-Beste-1234'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'sqlite:///' + os.path.join(basedir, 'user.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER=os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT=int(os.environ.get('MAIL_PORT')) or 465
    MAIL_USE_TLS = is.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'simon.vanharingen@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['thomas.erents@gmail.com']
    
