import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
#from User import User


class NN_Model(db.Model):
	__tablename__ = 'neural-networks'
	id = db.Column(db.Text, primary_key=True)
	name = db.Column(db.Text)
	algorithm_name = db.Column(db.Text, db.ForeignKey('algorithms.name')) #this determines the structure we'll use to push this model through.
	state = db.Column(db.Text)
	#events = db.relationship('Event_Model', backref='service', lazy = 'dynamic')
	positive_cases = db.relationship('NN_Positive_Service_Subscription', backref='neuralnets', cascade = 'all')
	negative_cases = db.relationship('NN_Negative_Service_Subscription', backref='neuralnets', cascade = 'all')

	def __init__(self, id, name, algorithm_name, state):
		self.id =  id
		self.name = name
		self.algorithm_name = algorithm_name
		self.state = state

	def __repr__(self):
		return '<NN: id {}>'.format(self.id)


class NN_Positive_Service_Subscription(db.Model):
	__tablename__ = 'nn-positive-service-subscriptions'
	service_name = db.Column(db.String(36), db.ForeignKey('services.name', ondelete = 'CASCADE'), primary_key = True)
	model_id = db.Column(db.String(36), db.ForeignKey('neural-networks.id', ondelete = 'CASCADE'), primary_key = True)

	def __init__(self, nn_model, service):
		self.model_name =  nn_model.id
		self.service_name = service.name

	def __init__(self, model_id, service_name):
		self.model_id =  model_id
		self.service_name = service_name

	def __repr__(self):
		return '<model {}>'.format(self.model_id) + ', <service {}>'.format(self.service_name)


class NN_Negative_Service_Subscription(db.Model):
	__tablename__ = 'nn-negative-service-subscriptions'
	service_name = db.Column(db.String(36), db.ForeignKey('services.name', ondelete = 'CASCADE'), primary_key = True)
	model_id = db.Column(db.String(36), db.ForeignKey('neural-networks.id', ondelete = 'CASCADE'), primary_key = True)

	def __init__(self, nn_model, service):
		self.model_id =  nn_model.id
		self.service_name = service.name

	def __init__(self, model_id, service_name):
		self.model_id =  model_id
		self.service_name = service_name

	def __repr__(self):
		return '<model {}>'.format(self.model_id) + ', <service {}>'.format(self.service_name)
