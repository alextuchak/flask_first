import hashlib
from sqlalchemy import exc
import config
import errors
import datetime
from app import db
from uuid import uuid4


class BaseModel:

    @classmethod
    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            return errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck


class User(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    token = db.Column(db.String(256), unique=True, index=True, default=uuid4())

    def __str__(self):
        return '<User {}'.format(self.username)

    def __repr__(self):
        return str(self)

    def set_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }


class Ads(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    descriptions = db.Column(db.String(512))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __str__(self):
        return 'ADS {}'.format(self.name)

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'descriptions': self.descriptions,
            'created': self.created,
            'owner': self.owner
        }
