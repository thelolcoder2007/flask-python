from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    admin_access = db.Column(db.Boolean)

    def __Repr__(self):
        return '<user {}>'.format(self.username)

def adduser(username, email, admin_access):
    u = User(username=username, email=email, admin_access=admin_access)
    db.session.add(u)
    db.session.commit()
