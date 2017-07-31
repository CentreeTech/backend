import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
import datetime
from dateutil.parser import parse

from Utility.color_print import ColorPrint
from Models.Event_Model import Event_Model
from Models.Device_Model import Device_Model, User_Device
from Models.User_Model import User_Model
from Models.Service_Model import Service_Model
#from sqlalchemy.types import Decimal 


#TODO figure out how to do DATABASE MIGRATIONS
#for this portion of the code, we will need to have dynamic code, 
#because it's going to be different structures for whichever event
#we are currently working on.


class Event():

	@staticmethod
	def list_device_events():
		if User_Model.authenticate_user(request.authorization):
			parsed_json = request.get_json()
			device_id = parsed_json["device_id"]
			db_device_events = Event_Model.query.join(Device_Model).filter(Device_Model.id == device_id).all()
			return_json_list = []
			for report in db_device_events:
				dict_local = {'report_id': report.report_id,
					  'reported_at': str(report.reported_at),
					  'type' : report.service_name}
				return_json_list.append(dict_local)
			return_string = json.dumps(return_json_list, sort_keys=True, indent=4, separators=(',', ': '))
			print("[DEBUG] - list_device_events: Successful")
			return return_string
		else:
			ColorPrint.print_message("Warning", "list_device_events", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def list_new_events():
		if User_Model.authenticate_user(request.authorization):
			auth = request.authorization
			parsed_json = request.get_json()
			timestamp = parsed_json["timestamp"] #this allows us to determine when new data is relevant.
			user_id = auth.username
			db_new_events = Event_Model.query.join(Device_Model).join(User_Device).filter(User_Device.user_name == user_id, Event_Model.reported_at > parse(timestamp) ).all()
			newest_event = Event_Model.query.join(Device_Model).join(User_Device).filter(User_Device.user_name == user_id).order_by(Event_Model.reported_at.desc()).first()
			return_json_dict = {}
			for report in db_new_events:
				dict_local = {'report_id': report.report_id,
					  'reported_at': str(report.reported_at),
					  'media': report.media,
					  'service_name' : report.service_name}
				if report.device_id in return_json_dict:
					return_json_dict[report.device_id][report.report_id] = dict_local
				else: 
					return_json_dict[report.device_id] =  {report.report_id : dict_local}
			if newest_event:
				most_recent_report = newest_event.reported_at
			else:
				most_recent_report = None
			dict_container = {'events': return_json_dict, 'most_recent_event_timestamp' : str(most_recent_report)}
			return_string = json.dumps(dict_container, sort_keys=True, indent=4, separators=(',', ': '))
			print("[DEBUG] - list_new_events: Successful")
			return return_string
		else:
			ColorPrint.print_message("Warning", "list_device_events", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def add_device_event():
		if Device_Model.authenticate_device(request.authorization):
			auth = request.authorization
			device_id = auth.username
			parsed_json = request.get_json()
			report_id = str(uuid.uuid4())
			service_name = parsed_json["service_name"]
			if not Service_Model.query.filter_by(name = service_name).scalar():
				dict_local = {'code': 31, 'message': "Service does not exist."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			event = Event_Model(report_id, device_id, service_name, "mp4")
			db.session.add(event)
			db.session.commit()
			dict_local = {'report_id': report_id, 'device_id': device_id}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			ColorPrint.print_message("Warning", "add_device_event", "Device Authentication Failed")
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

app.add_url_rule('/list_device_events', 'list_device_events', Event.list_device_events, methods=['POST'])
app.add_url_rule('/list_new_events', 'list_new_events', Event.list_new_events, methods=['POST'])
app.add_url_rule('/add_device_event', 'add_device_event', Event.add_device_event, methods=['POST'])

