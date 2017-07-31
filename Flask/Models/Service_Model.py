import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
#from User import User


class Service_Model(db.Model):
	__tablename__ = 'services'
	name = db.Column(db.String(36), primary_key=True)
	#events = db.relationship('Event_Model', backref='service', lazy = 'dynamic')
	users = db.relationship('User_Subscription', backref='service', cascade = 'all')
	devices = db.relationship('Device_Subscription', backref='service', cascade = 'all')
	_events = db.relationship('Event_Model', backref = 'service')
	_classifications = db.relationship('Classification_Model', backref = 'service')
	_enums = db.relationship('Enum', backref = "service", cascade = 'all')

	nn_pos_model = db.relationship('NN_Positive_Service_Subscription', backref='service', cascade = 'all')
	nn_neg_model = db.relationship('NN_Negative_Service_Subscription', backref='service', cascade = 'all')

	def __init__(self, name):
		self.name =  name

	def __repr__(self):
		return '<service {}>'.format(self.name)


class Enum(db.Model):
	__tablename__ = 'enums'
	id = db.Column(db.String(36), primary_key = True)
	service_name = db.Column(db.String(36), db.ForeignKey('services.name', ondelete = 'CASCADE'))
	name = db.Column(db.String(36))
	entry_id = db.relationship('Enum_Entry', backref = 'enum', cascade = 'all')


	def __init__(self, id, name, service_name):
		self.id = id
		self.name =  name
		self.service_name = service_name

	def __repr__(self):
		return '<enum {}'.format(self.id) + ', name {}>'.format(self.name)


class Enum_Entry(db.Model):
	__tablename__ = 'enum-entries'
	id = db.Column(db.String(36), primary_key = True)
	value = db.Column(db.String(36))
	enum_id = db.Column(db.String(36), db.ForeignKey('enums.id', ondelete = 'CASCADE'))

	def __init__(self, id, value, enum_id):
		self.id = id
		self.value = value
		self.enum_id = enum_id

	def __repr__(self):
		return '<value {}>'.format(self.value)


class User_Subscription(db.Model):
	__tablename__ = 'user-subscriptions'
	user_name = db.Column(db.String(36), db.ForeignKey('users.name', ondelete = 'CASCADE'), primary_key = True)
	service_name = db.Column(db.String(36), db.ForeignKey('services.name', ondelete = 'CASCADE'), primary_key = True)

	def __init__(self, user, service):
		self.user_name =  user.name
		self.service_name = service.name

	def __init__(self, user_name, service_name):
		self.user_name =  user_name
		self.service_name = service_name

	def __repr__(self):
		return '<user {}>'.format(self.user_name) + ', <service {}>'.format(self.service_name)


class Device_Subscription(db.Model):
	__tablename__ = 'device-subscriptions'
	device_id = db.Column(db.String(36), db.ForeignKey('devices.id'), primary_key = True)
	service_name = db.Column(db.String(36), db.ForeignKey('services.name'), primary_key = True)
	device = db.relationship('Device_Model', backref='services')

	def __init__(self, device, service):
		self.device_id = device.id
		self.service_name = service.name

	def __init__(self, device_id, service_name):
		self.device_id = device_id
		self.service_name = service_name

	def __repr__(self):
		return '<device {}>'.format(self.device_id) + ', <service {}>'.format(self.service_name)






