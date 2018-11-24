from kamericanapp import db
from datetime import datetime
from sqlalchemy.sql import expression
from sqlalchemy.ext.hybrid import hybrid_property
from pathlib import Path


class Group(db.Model):
    """Database table of groups"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # One group to many identities
    identities = db.relationship('Identity', back_populates='group') # this is a query of all identities, not a field
    
    def __repr__(self):
        return '<Group: {0}>'.format(self.name)

class Identity(db.Model):
    """Database table of identities"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # One identity to many faces
    faces = db.relationship('Face', back_populates='identity') # this is a query of all faces with this identity id, not a field
    # Each identity has a group
    group_id = db.Column(db.Integer, db.ForeignKey('group.id')) # this is what Group.identities is querying for
    group = db.relationship('Group', back_populates='identities')

    def __repr__(self):
        return '<Name: {0} ({1})>'.format(
            self.name,
            self.group.name,
        )

class Image(db.Model):
    """Database table of images"""
    id = db.Column(db.Integer, primary_key=True)
    _filepath_original = db.Column(db.String)
    _filepath_resize = db.Column(db.String)
    filename = db.Column(db.String)
    faces_extracted = db.Column(db.Boolean, default=False, server_default=expression.false(), nullable=False)
    # One image to many faces
    faces = db.relationship('Face', back_populates='image') # this is a query of all faces with this image id, not a field
    
    # File paths
    @hybrid_property
    def filepath_original(self):
        if self._filepath_original is None:
            return None
        else:
            return Path(self._filepath_original)
    @filepath_original.setter
    def filepath_original(self, path):
        self._filepath_original = str(path)
    
    @hybrid_property
    def filepath_resize(self):
        if self._filepath_resize is None:
            return None
        else:
            return Path(self._filepath_resize)
    @filepath_resize.setter
    def filepath_resize(self, path):
        self._filepath_resize = str(path)

    # Methods
    def __repr__(self):
        return '<Image: {0}>'.format(self.filename)

class Face(db.Model):
    """Database table of faces"""
    id = db.Column(db.Integer, primary_key=True)
    embedding = db.Column(db.PickleType)
    _filepath = db.Column(db.String)
    # Each face has an identity
    identity_id = db.Column(db.Integer, db.ForeignKey('identity.id')) # this is what identity.faces is querying for
    identity =  db.relationship('Identity', back_populates='faces')
    # Each face has an image
    image_id = db.Column(db.Integer, db.ForeignKey('image.id')) # this is what Image.faces is querying for
    image = db.relationship('Image', back_populates='faces')
    # add training/predicted stuff here
    
    @hybrid_property
    def filepath(self):
        if self._filepath is None:
            return None
        else:
            return Path(self._filepath)
    @filepath.setter
    def filepath(self, path):
        self._filepath = str(path)

    def __repr__(self):
        return '<Face: {0}>'.format(self.identity)

class RQJob(db.Model):
    """Database table of redis queue worker jobs"""
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36))
    process = db.Column(db.String(72))
    status = db.Column(db.String(8))
    enqueued_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    result =  db.Column(db.String(128))

    def __repr__(self):
        return '<Job ID: {0}, Process: {1}>'.format(self.job_id, self.process)

    def save_job(self, job):
        """Save job details to the RQJob db table""" 
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
    def get_result(self):
        """Return job result"""
        if self.result is None:
            return "Job has no result"
        else:
            return self.result
    def get_elapsed_time(self):
        """Return job run time"""
        time_delta = self.ended_at - self.started_at
        return time_delta.seconds