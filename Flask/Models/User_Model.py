import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime


class User_Model(db.Model):
    __tablename__ = 'users'

    name = db.Column(db.String(36), primary_key=True)
    password = db.Column(db.String(36))
    email = db.Column(db.String(36))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    account_type = db.Column(db.String(36))
    services = db.relationship('User_Subscription', backref='user', cascade = 'all')
    devices = db.relationship('User_Device', backref='user', cascade = 'all')

    def __init__(self, name, password, email, account_type):
        self.name = name
        self.password = password
        self.email = email
        #self.created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        self.account_type = account_type

    def __repr__(self):
        return '<name {}>'.format(self.name)

    @staticmethod
    def authenticate_user(auth):
        if not auth:
            return False
        password = auth.password
        name = auth.username
        user_info = User_Model.query.filter_by(name = name).first()
        if user_info is None:
            return False
        if user_info.password is not None:
            if user_info.password == password:
                return True
        return False
