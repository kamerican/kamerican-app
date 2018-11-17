from kamericanapp import db
from datetime import datetime

class RQJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36))
    process = db.Column(db.String(72))
    status = db.Column(db.String(8))
    enqueued_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    result =  db.Column(db.String(128))

    def __repr__(self):
        return '<ID: {0}, Process: {1}>'.format(self.job_id, self.process)

    def save_job(self, job):
        self.job_id = job.id
        self.status = job.status
        self.enqueued_at = job.enqueued_at
        self.started_at = job.started_at
        self.ended_at = job.ended_at
        self.result = job.result
        if 'process' in job.meta:
            self.process = job.meta['process']
        else:
            print("@@@ Job to be saved does not have a process in job.meta @@@")
            self.process = "No process saved"
        db.session.add(self)
        db.session.commit()
    def get_id(self):
        return self.job_id
    def get_process(self):
        return self.process
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
    def get_elapsed_time(self):
        time_delta = self.ended_at - self.started_at
        return time_delta.seconds