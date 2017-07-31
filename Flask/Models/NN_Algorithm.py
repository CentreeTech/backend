import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
#from User import User


class NN_Algorithm(db.Model):
	__tablename__ = 'algorithms'
	name = db.Column(db.Text, primary_key = True) #this determines the structure we'll use to push this model through.
	description = db.Column(db.Text)
	_models = db.relationship('NN_Model', backref='algorithm')

	def __init__(self, name, description):
		self.name = name
		self.description = description

	def __repr__(self):
		return '<NN: algorithm_name {}>'.format(self.algorithm_name)