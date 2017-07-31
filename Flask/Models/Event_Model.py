import sys
import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime

class Event_Model(db.Model):
    __tablename__ = 'events'
    report_id = db.Column(db.String(36), primary_key=True)
    reported_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id'))
    service_name = db.Column(db.String(36), db.ForeignKey('services.name'))
    media = db.Column(db.Text)
    #service
    #device

    def __init__(self, report_id, device_id, service_name, media):
        self.report_id = report_id
        self.device_id = device_id
        self.service_name = service_name
        self.media = media

    def __repr__(self):
        return '<device_id {}>'.format(self.device_id)
