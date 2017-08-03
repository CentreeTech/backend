import requests
import base64
import json
import time
import sys
import importlib

import NN_Models.BaseModel

#returns the algorithm name, the model to update
#and the services useful for updating.
#if None then no models needed updating.


user_name = "USERNAME"
password = "PASSWORD"

production = False

if (production):
	MODELS_TO_UPDATE_URL = "http://backend.centree.xyz:5000/get_model_to_update"
	GET_RELEVANT_CLASSIFICATIONS_URL = "http://backend.centree.xyz:5000/get_relevant_classifications"
	GET_DATA_CRED_URL = "http://backend.centree.xyz:5000/get_data_storage_credentials"
else:
	MODELS_TO_UPDATE_URL = "http://localhost:5000/get_model_to_update"
	GET_RELEVANT_CLASSIFICATIONS_URL = "http://localhost:5000/get_relevant_classifications"
	GET_DATA_CRED_URL = "http://localhost:5000/get_data_storage_credentials"

verbose = False

def get_model_to_update():
	model = requests.get(MODELS_TO_UPDATE_URL, auth = requests.auth.HTTPBasicAuth(user_name, password))
	model_dict = json.loads(model.text)
	return model_dict

def getClassifications(service_names):
	returnJson = {'service_names': service_names}
	returnstring = json.dumps(returnJson, sort_keys=True, indent=4, separators=(',', ': '))
	headers = {'content-type': 'application/json'}
	classifications = requests.post(GET_RELEVANT_CLASSIFICATIONS_URL, data = returnstring, 
		auth = requests.auth.HTTPBasicAuth(user_name, password), headers = headers)
	classifications = json.loads(classifications.text)
	return classifications


def get_data_storage_credentials():
	model = requests.get(GET_DATA_CRED_URL, auth = requests.auth.HTTPBasicAuth(user_name, password))
	return json.loads(model.text)


if __name__ == "__main__":

	running = True

	while (running):
		time.sleep(3)
		#check to see if there needs to be an update.
		model_info = get_model_to_update()
		if "code" in model_info.keys() and model_info["code"] == 31:
			print (model_info["message"])
			continue
		#if the update is necessary then grab classification data.
		classifications = getClassifications(model_info["positive_cases"] + model_info["negative_cases"])
		if verbose: print("CLASSIFICATIONS\n" + str(classifications))

		#get model_builder
		algorithm_name = model_info["algorithm_name"]
		module = importlib.import_module('NN_Models.'+ algorithm_name)
		model_class = getattr(module, algorithm_name)

		s3_login_info = get_data_storage_credentials()

		if verbose: print( "LOGIN INFO\n" + str(s3_login_info))

		model = model_class(classifications, model_info, s3_login_info)
		
		#build model

		model.train()

		#train

		#model.train()

		#export







