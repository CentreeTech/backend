import json
import uuid
from flaskapp import db, app
from User import User
from Device import Device
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import func
from flask import request, Response, send_file, send_from_directory
import datetime
from Utility.color_print import ColorPrint
from Models.User_Model import User_Model
from Models.Classification_Model import Classification_Model, String_Attribute, Classification_To_String_Attribute
from Models.Service_Model import Service_Model, Enum, Enum_Entry
from Models.NN_Model import NN_Model, NN_Positive_Service_Subscription, NN_Negative_Service_Subscription
from Models.NN_Algorithm import NN_Algorithm

class Generate():

	# @staticmethod
	# def add_new_model():
	# 	if User_Model.authenticate_user(request.authorization):
	# 		auth = request.authorization
	# 		user_id = auth.username
	# 		request_json = request.get_json()
	# 		# session.query(Record).filter(Record.id.in_(seq)).all()
	# 		positive_cases = request_json["positive_cases"]
	# 		negative_cases = request_json["negative_cases"]
	# 		algorithm_name = request_json["algorithm_name"]

	# 		pos_cas = Service_Model.query.filter(Service_Model.name.in_(positive_cases)).all()

	# 		if len(positive_cases) != len(pos_cas):
	# 			dict_local = {'code': 31, 'message': "A service does not exist."}
	# 			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
	# 			return return_string

	# 		neg_cas = Service_Model.query.filter(Service_Model.name.in_(negative_cases)).all()

	# 		if len(negative_cases) != len(neg_cas):
	# 			dict_local = {'code': 31, 'message': "A service does not exist."}
	# 			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
	# 			return return_string

	# 		model = NN_Model.query.join(NN_Positive_Service_Subscription).join(NN_Negative_Service_Subscription).filter(
	# 			NN_Positive_Service_Subscription.service_name.in_(positive_cases),
	# 			NN_Negative_Service_Subscription.service_name.in_(negative_cases),
	# 			NN_Model.algorithm_name == algorithm_name
	# 			).first()

	# 		if not model: #then this model doesn't exist yet
	# 			model_id = uuid.uuid4()
	# 			new_model = NN_Model(model_id, algorithm_name, "NEEDS_UPDATE")
	# 			db.session.add(new_model)
	# 			for positive_case in positive_cases:
	# 				#start adding subscriptions
	# 				pos_sub = NN_Positive_Service_Subscription(model_id, positive_case)
	# 				db.session.add(pos_sub)
	# 			for negative_case in negative_cases:
	# 				#start adding subscriptions
	# 				neg_sub = NN_Negative_Service_Subscription(model_id, negative_case)
	# 				db.session.add(neg_sub)
	# 		elif model.state == "GENERATING":
	# 			dict_local = {'code': 31, 'message': "Model is already generating"}
	# 			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
	# 			return return_string
	# 		elif model.state == "NEEDS_UPDATE":
	# 			dict_local = {'code': 31, 'message': "Model already needs update."}
	# 			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
	# 			return return_string
	# 		else:
	# 			model.state = "NEEDS_UPDATE"
	# 		db.session.commit()
	# 		dict_local = {'code': 200}
	# 		return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
	# 		return return_string
	# 	else:
	# 		ColorPrint.print_message("Warning", "generate_model", "User Authentication Failed")
	# 		dict_local = {'code': 31, 'message': "user authentication failed"}
	# 		return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
	# 		return return_string

	@staticmethod
	def add_new_model():
		if User_Model.authenticate_user(request.authorization):
			auth = request.authorization
			user_id = auth.username
			request_json = request.get_json()
			positive_cases = request_json["positive_cases"]
			negative_cases = request_json["negative_cases"]
			algorithm_name = request_json["algorithm_name"]
			model_name = request_json["model_name"]
			pos_cas = Service_Model.query.filter(Service_Model.name.in_(positive_cases)).all()
			if len(positive_cases) != len(pos_cas):
				dict_local = {'code': 31, 'message': "A service does not exist."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			neg_cas = Service_Model.query.filter(Service_Model.name.in_(negative_cases)).all()
			if len(negative_cases) != len(neg_cas):
				dict_local = {'code': 31, 'message': "A service does not exist."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			if not NN_Algorithm.query.filter_by(name = algorithm_name).scalar():
				dict_local = {'code': 31, 'message': "The algorithm does not exist."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			model_id = uuid.uuid4()
			new_model = NN_Model(model_id, model_name, algorithm_name, "NEEDS_UPDATE")
			db.session.add(new_model)
			for positive_case in positive_cases:
				#start adding subscriptions
				pos_sub = NN_Positive_Service_Subscription(model_id, positive_case)
				db.session.add(pos_sub)
			for negative_case in negative_cases:
				#start adding subscriptions
				neg_sub = NN_Negative_Service_Subscription(model_id, negative_case)
				db.session.add(neg_sub)
			db.session.commit()
			dict_local = {'code': 200}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			ColorPrint.print_message("Warning", "generate_model", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	#pointless fucking method
	@staticmethod
	def model_exists():
		if User_Model.authenticate_user(request.authorization):
			auth = request.authorization
			user_id = auth.username
			request_json = request.get_json()
			# session.query(Record).filter(Record.id.in_(seq)).all()
			positive_cases = request_json["positive_cases"]
			negative_cases = request_json["negative_cases"]
			algorithm_name = request_json["algorithm_name"]

			if NN_Algorithm.query.filter_by(name = algorithm_name).scalar():
				dict_local = {'code': 31, 'message': "Algorithm doesn't exist."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string

			if len(positive_cases) == 0:
				if len(negative_cases == 0):
					model = NN_Model.query.join(NN_Positive_Service_Subscription).join(NN_Negative_Service_Subscription).filter(
						NN_Model.algorithm_name == algorithm_name
						).scalar()
				else:
					model = NN_Model.query.join(NN_Positive_Service_Subscription).join(NN_Negative_Service_Subscription).filter(
						NN_Negative_Service_Subscription.service_name.in_(negative_cases),
						NN_Model.algorithm_name == algorithm_name
						).scalar()
			elif len(negative_cases) == 0:
				model = NN_Model.query.join(NN_Positive_Service_Subscription).join(NN_Negative_Service_Subscription).filter(
						NN_Positive_Service_Subscription.service_name.in_(positive_cases),
						NN_Model.algorithm_name == algorithm_name
						).scalar()

			if model:
				dict_local = {'code': 200}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			else:
				dict_local = {'code': 31, 'message': "Model does not exist."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
		else:
			ColorPrint.print_message("Warning", "model_exists", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string


	@staticmethod
	def get_models_under_constraint():
		if User_Model.authenticate_user(request.authorization):
			auth = request.authorization
			user_id = auth.username
			request_json = request.get_json()
			# session.query(Record).filter(Record.id.in_(seq)).all()
			positive_cases = request_json["positive_cases"]
			negative_cases = request_json["negative_cases"]

			if len(positive_cases) == 0:
				if len(negative_cases) == 0:
					models = NN_Model.query.all()
				else:
					models = NN_Model.query.join(NN_Positive_Service_Subscription).join(NN_Negative_Service_Subscription).filter(
						NN_Negative_Service_Subscription.service_name.in_(negative_cases)
						).scalar()
			elif len(negative_cases) == 0:
				models = NN_Model.query.join(NN_Positive_Service_Subscription).join(NN_Negative_Service_Subscription).filter(
						NN_Positive_Service_Subscription.service_name.in_(positive_cases)
						).all()
			else:
				models = NN_Model.query.join(NN_Positive_Service_Subscription).join(NN_Negative_Service_Subscription).filter(
						NN_Positive_Service_Subscription.service_name.in_(positive_cases),
						NN_Negative_Service_Subscription.service_name.in_(negative_cases)
						).all()

			return_dict = {}

			for model in models:
				positives = []
				for pcases in model.positive_cases:
					positives += [ pcases.service_name]
				negatives = []
				for ncases in model.negative_cases:
					negatives += [ ncases.service_name]
				return_dict[model.id] = {"algorithm_name" : model.algorithm_name, 
							"state" : model.state,
							"positive_cases" : positives,
							"negative_cases" : negatives,
							"model_name" : model.name}
			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			ColorPrint.print_message("Warning", "model_exists", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string


	@staticmethod
	def delete_model():
		if User_Model.authenticate_user(request.authorization):
			auth = request.authorization
			user_id = auth.username
			request_json = request.get_json()
			# session.query(Record).filter(Record.id.in_(seq)).all()
			model_id = request_json["model_id"]

			model = NN_Model.query.filter_by(id = model_id).first()

			if model:
				db.session.delete(model)
				db.session.commit()
				dict_local = {'code': 200}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			else:
				dict_local = {'code': 31, 'message': "Model does not exist."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
		else:
			ColorPrint.print_message("Warning", "delete_model", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def get_model_to_update():
		if User_Model.authenticate_user(request.authorization):
			auth = request.authorization
			user_id = auth.username

			model = NN_Model.query.filter_by(state = "NEEDS_UPDATE").first()

			if model:
				positives = []
				for pcases in model.positive_cases:
					positives += [ pcases.service_name]
				negatives = []
				for ncases in model.negative_cases:
					negatives += [ ncases.service_name]
				return_dict = { "id" : model.id,
							"algorithm_name" : model.algorithm_name, 
							"state" : model.state,
							"positive_cases" : positives,
							"negative_cases" : negatives}

				return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			else:
				dict_local = {'code': 31, 'message': "No models need to be updated."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
		else:
			ColorPrint.print_message("Warning", "delete_model", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def list_all_models():
		if User_Model.authenticate_user(request.authorization):
			models = NN_Model.query.all()
			return_dict = {}
			for model in models:
				positives = []
				for pcases in model.positive_cases:
					positives += [ pcases.service_name]
				negatives = []
				for ncases in model.negative_cases:
					negatives += [ ncases.service_name]
				return_dict[model.id] = {"algorithm_name" : model.algorithm_name, 
							"state" : model.state,
							"positives" : positives,
							"negatives" : negatives}
			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			ColorPrint.print_message("Warning", "generate_model", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def add_new_algorithm():
		if User_Model.authenticate_user(request.authorization):
			auth = request.authorization
			user_id = auth.username
			request_json = request.get_json()
			description = request_json["description"]
			algorithm_name = request_json["algorithm_name"]
			algorithms = NN_Algorithm.query.filter(NN_Algorithm.name == algorithm_name).scalar()
			if not algorithms:
				_algorithm = NN_Algorithm(algorithm_name, description)
				db.session.add(_algorithm)
				db.session.commit()
				dict_local = {'code': 200}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			else:
				dict_local = {'code': 31, 'message': 'An algorithm with this name already exists.'}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
		else:
			ColorPrint.print_message("Warning", "generate_model", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def list_all_algorithms():
		if User_Model.authenticate_user(request.authorization):
			algorithms = NN_Algorithm.query.all()
			return_dict = {}
			for algorithm in algorithms:
				return_dict[algorithm.name] = {"description" : algorithm.description}
			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			ColorPrint.print_message("Warning", "generate_model", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def remove_algorithm():
		if User_Model.authenticate_user(request.authorization):
			auth = request.authorization
			user_id = auth.username
			request_json = request.get_json()
			algorithm_name = request_json["algorithm_name"]
			algorithm = NN_Algorithm.query.filter(NN_Algorithm.name == algorithm_name).first()
			if algorithm:
				db.session.delete(algorithm)
				db.session.commit()
				dict_local = {'code': 200}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			else:
				dict_local = {'code': 31, 'message' : 'Algorithm didn\'t exist anyways.'}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
		else:
			ColorPrint.print_message("Warning", "generate_model", "User Authentication Failed")
			dict_local = {'code': 31, 'message': "user authentication failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

app.add_url_rule('/add_new_model', 'add_new_model', Generate.add_new_model, methods=['POST'])
app.add_url_rule('/model_exists', 'model_exists', Generate.model_exists, methods=['POST'])
app.add_url_rule('/delete_model', 'delete_model', Generate.delete_model, methods=['POST'])
app.add_url_rule('/list_all_models', 'list_all_models', Generate.list_all_models, methods=['GET'])

app.add_url_rule('/get_model_to_update', 'get_model_to_update', Generate.get_model_to_update, methods=['GET'])
app.add_url_rule('/get_models_under_constraint', 'get_models_under_constraint', Generate.get_models_under_constraint, methods=['POST'])

app.add_url_rule('/add_new_algorithm', 'add_new_algorithm', Generate.add_new_algorithm, methods=['POST'])
app.add_url_rule('/list_all_algorithms', 'list_all_algorithms', Generate.list_all_algorithms, methods=['GET'])
app.add_url_rule('/remove_algorithm', 'remove_algorithm', Generate.remove_algorithm, methods=['POST'])
