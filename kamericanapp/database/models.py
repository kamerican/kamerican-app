from kamericanapp import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash





# UNUSED TABLE
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    perm_twtimgdl = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.email)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
