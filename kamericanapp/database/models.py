from kamericanapp import db
from datetime import datetime
import enum

class Identity(enum.Enum):
    # WJSN
    WJSN_SEOLA = enum.auto()
    WJSN_XUANYI = enum.auto()
    WJSN_BONA = enum.auto()
    WJSN_EXY = enum.auto()
    WJSN_SOOBIN = enum.auto()
    WJSN_LUDA = enum.auto()
    WJSN_DAWON = enum.auto()
    WJSN_EUNSEO = enum.auto()
    WJSN_CHENGXIAO = enum.auto()
    WJSN_MEIQI = enum.auto()
    WJSN_YEOREUM = enum.auto()
    WJSN_DAYOUNG = enum.auto()
    WJSN_YEONJUNG = enum.auto()
    # Fromis
    FROMIS_SAEROM = enum.auto()

    def describe(self):
        return "name={0}, value={1}".format(self.name, self.value)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.Enum(Identity))
    name = db.Column(db.String)
    faces = db.relationship('Face', back_populates='person') # this is a query of all faces with this person id, not a field
    

    def __repr__(self):
        return '<Person: {0}>'.format(self.identity.describe())

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String)
    faces = db.relationship('Face', back_populates='image') # this is a query of all faces with this image id, not a field

    def __repr__(self):
        return '<Image: {0}>'.format(self.filepath)

class Face(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    embedding = db.Column(db.PickleType)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id')) # this is what Person.faces is querying for
    person =  db.relationship('Person', back_populates='faces')
    image_id = db.Column(db.Integer, db.ForeignKey('image.id')) # this is what Image.faces is querying for
    image = db.relationship('Image', back_populates='faces')
    # add training/predicted stuff here
    
    def __repr__(self):
        return '<Face: {0}>'.format(self.person)



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