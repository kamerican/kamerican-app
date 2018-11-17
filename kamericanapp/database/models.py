from kamericanapp import db
from datetime import datetime

class RQJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36))
    status = db.Column(db.String(8))
    enqueued_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<RQJob id: {}>'.format(self.job_id)
    
    def save_job(self, job):
        self.job_id = job.id
        self.status = job.status
        self.enqueued_at = job.enqueued_at
        self.started_at = job.started_at
        self.ended_at = job.ended_at
        self.result = job.result
        db.session.add(self)
        db.session.commit()
    def get_id(self):
        return self.job_id
    def get_status(self):
        return self.status
    def get_enqueue_time(self):
        return self.enqueued_at
    def get_start_time(self):
        return self.started_at
    def get_end_time(self):
        return self.ended_at
    def get_result(self):
        if self.result is None:
            return "Job has no result"
        else:
            return self.result


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
