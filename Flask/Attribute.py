import sys
import json
import uuid
from flaskapp import db, app
from User import User
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from color_print import ColorPrint


class Numeric_Attribute(db.Model):
	__tablename__ = 'numeric_attribute'

	name = db.Column(db.String(36))



class String_Attribute(db.Model):
	__tablename__ = 'string_attribute'