import json
import uuid
from flaskapp import db, app
from Models.Event_Model import Event_Model
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
import datetime
from Utility.color_print import ColorPrint
from Models.User_Model import User_Model
from Models.Config_Model import Config_Model

class Cloud_Storage():

	def get_data_storage_credentials():
		if User_Model.authenticate_user(request.authorization):
			aws_access = Config_Model.query.filter_by(name = 'AWS_ACCESS_KEY_ID').first()
			aws_secret = Config_Model.query.filter_by(name = 'AWS_SECRET_ACCESS_KEY').first()
			bucket = Config_Model.query.filter_by(name = 'BUCKET_NAME').first()
			dict_container = {"AWS_ACCESS_KEY_ID" : aws_access.value, "AWS_SECRET_ACCESS_KEY" : aws_secret.value, "BUCKET_NAME" : bucket.value}
			return_string = json.dumps(dict_container, sort_keys=True, indent=4, separators=(',', ': '))
			print("[DEBUG] - list_new_events: Successful")
			return return_string
		else:
			ColorPrint.print_message("Warning", "list_device_events", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

app.add_url_rule('/get_data_storage_credentials', 'get_data_storage_credentials', Cloud_Storage.get_data_storage_credentials, methods=['GET'])