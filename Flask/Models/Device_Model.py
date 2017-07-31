import sys
import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint

class Device_Model(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.String(36), primary_key=True)
    password = db.Column(db.String(36))
    _owners = db.relationship('User_Device', backref='device', cascade = 'all')
    _events = db.relationship('Event_Model', backref='device')
    software_version = db.Column(db.Numeric(3, 2))
    location = db.Column(db.String(36))
    name = db.Column(db.String(36))
    #events = db.relationship('Event_Model', backref='device', lazy='dynamic')

    def __init__(self, id, password, owner, software_version, location, name):
        self.id = id
        self.password = password
        self.owner = owner
        self.software_version = software_version
        self.location = location
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def authenticate_device(auth):
        password = auth.password
        id = auth.username
        db_device = Device_Model.query.filter_by(id = id).first()
        if db_device is None:
            ColorPrint.print_message("Warning", "authenticate_device", "Authentication Failed, Wrong Password")
            return False
        if db_device.password is not None:
            if db_device.password == password:
                return True
            else:
                ColorPrint.print_message("Warning", "authenticate_device", "Authentication Failed, Wrong Password")
                return False
        else:
            ColorPrint.print_message("Warning", "authenticate_device", "Authentication Failed, no device")
            return False



class User_Device(db.Model):
    __tablename__ = 'user-devices'
    user_name = db.Column(db.String(36), db.ForeignKey('users.name', ondelete = 'CASCADE'), primary_key = True)
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id', ondelete = 'CASCADE'), primary_key = True)
    owners = db.relationship('Device_Model', backref='owners')

    def __init__(self, user, device):
        self.user_name =  user.name
        self.device_id = device.id

    def __init__(self, user_name, device_id):
        self.user_name =  user_name
        self.device_id = device_id

    def __repr__(self):
        return '<user {}>'.format(self.user_name) + ', <device {}>'.format(self.device_id)



