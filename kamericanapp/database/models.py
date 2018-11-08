from kamericanapp import db
from datetime import datetime

from rq import Queue, get_current_job
from redis import Redis
from rq.job import Job
from rq.registry import StartedJobRegistry, FinishedJobRegistry




class RQJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36))
    status = db.Column(db.String(8))
    enqueued_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<RQJob id: {}>'.format(self.job_id)
    def set_status(self, job_status):
        self.status = job_status
    def set_enqueue_time(self, rq_time):
        self.enqueued_at = rq_time
    def set_start_time(self, rq_time):
        self.started_at = rq_time
    def set_end_time(self, rq_time):
        self.ended_at = rq_time
    def get_enqueue_time(self):
        return self.enqueued_at
    def get_start_time(self):
        return self.started_at
    def get_end_time(self):
        return self.ended_at


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
