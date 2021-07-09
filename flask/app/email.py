from flask_mail import Message, Mail
from flask import render_template
from app import mail

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Fleur home]: reset your password', sender=app.config['MAIL_USERNAME'], recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token))
