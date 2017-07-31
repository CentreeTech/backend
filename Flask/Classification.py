import json
import uuid
from flaskapp import db, app
from User import User
from Device import Device
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
import datetime
from Utility.color_print import ColorPrint
from Models.User_Model import User_Model
from Models.Classification_Model import Classification_Model, String_Attribute, Classification_To_String_Attribute
from Models.Service_Model import Service_Model, Enum, Enum_Entry

class Classification():

    @staticmethod
    def bad_attribute(method):
        dict_local = {'code': 31, 'message': "bad attribute"}
        return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
        return return_string

    @staticmethod
    def add_classifications():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            classifications = request.get_json()
            # session.query(Record).filter(Record.id.in_(seq)).all()
            attributes_to_commit = []
            classifications_to_commit = []
            for classification in classifications:
                if not "service" in classification:
                    dict_local = {'code': 31, 'message': "no service field"}
                    return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                    return return_string
                service_name = classification["service"]
                service = Service_Model.query.filter_by(name = service_name).first()
                if service:
                    enums = Enum.query.join(Service_Model).filter(Service_Model.name == service_name).all()
                    try:
                        attributes = classification["attributes"]
                        class_id = str(uuid.uuid4())
                        start_time = classification["start_time"]
                        stop_time = classification["end_time"]
                        media = classification["media"]
                    except KeyError:
                        return_json = {'code': 31, 'message' : 'One or more key in the API body is bad.'}
                        return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                        return return_string
                    _class = Classification_Model(class_id,service_name, start_time, stop_time, media)
                    classifications_to_commit += [_class]
                    for enum in enums:
                        if enum.name in attributes.keys():
                            #then this is an attribute, so we need to convert it to a string attribute.
                            value = attributes[enum.name]
                            attribute = String_Attribute.query.filter(String_Attribute.name == enum.name, String_Attribute.value == value).first()
                            if not attribute:
                                #it doesn't yet exist
                                stat_id = str(uuid.uuid4())
                                attribute = String_Attribute(stat_id, enum.name, value)
                                attributes_to_commit += [attribute]
                            else:
                                c_to_sa = Classification_To_String_Attribute(_class.id, attribute.id)
                        else:
                            #bad attribute
                            ColorPrint.print_message("Error", "add_classifications", "enum name not in attributes: " + enum.name)
                            return Classification.bad_attribute(Classification.add_classifications)
                        enum_entries = Enum_Entry.query.join(Enum).filter(Enum.id == enum.id).all()
                else:
                    #ColorPrint.print_message("Debug", "register_account_user", "email already exists")
                    return_json = {'code': 31, 'message': "A service does not exist."}
                    return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                    return return_string
            for at_2_c in attributes_to_commit:
                db.session.add(at_2_c)
            for at_2_c in classifications_to_commit:
                db.session.add(at_2_c)
            db.session.commit()
            return_json = {'code': 200, 'id' : class_id}
            return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
            print("[DEBUG] - add_classifications: Successful")
            return return_string    
        else:
            ColorPrint.print_message("Warning", "add_classifications", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def get_classifications():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            classification_ids = request.get_json()
            reports = Classification_Model.query.filter(Classification_Model.id.in_(classification_ids)).all()
            return_json_array = []
            for report in reports:
                dict_local = {'id': str(report.id),
                              'start_time' : report.start_time,
                              'stop_time' : report.stop_time,
                              'service' : report.service_name,
                              'media' : report.media}
                return_json_array += [dict_local]
            return_string = json.dumps(return_json_array, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            ColorPrint.print_message("Warning", "add_classifications", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def get_all_classifications():
        if User_Model.authenticate_user(request.authorization):
            reports = Classification_Model.query.all()
            return_json_array = []
            for report in reports:
                dict_local = {'id': str(report.id),
                              'start_time': report.start_time,
                              'stop_time' : report.stop_time,
                              'service' : report.service_name,
                              'media' : report.media}
                return_json_array += [dict_local]
            return_string = json.dumps(return_json_array, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            ColorPrint.print_message("Warning", "add_classifications", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_new_filename():
        if User_Model.authenticate_user(request.authorization):
            return_json_array = {'filename' : str(uuid.uuid4())}
            return_string = json.dumps(return_json_array, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            ColorPrint.print_message("Warning", "add_classifications", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def get_relevant_classifications():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            request_json = request.get_json()
            service_names = request_json["service_names"]
            json_dict = {}
            reports = Classification_Model.query.filter(Classification_Model.service_name.in_(service_names)).all()
            return_json_array = []
            for report in reports:
                dict_local = {'id': str(report.id),
                              'start_time': report.start_time,
                              'stop_time' : report.stop_time,
                              'service' : report.service_name,
                              'media' : report.media}
                return_json_array += [dict_local]
            return_string = json.dumps(return_json_array, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            ColorPrint.print_message("Warning", "add_classifications", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string



app.add_url_rule('/add_classifications', 'add_classifications', Classification.add_classifications, methods=['POST'])
app.add_url_rule('/get_classifications', 'get_classifications', Classification.get_classifications, methods=['POST'])
app.add_url_rule('/get_all_classifications', 'get_all_classifications', Classification.get_all_classifications, methods=['GET'])
app.add_url_rule('/get_new_filename', 'get_new_filename', Classification.get_new_filename, methods=['GET'])

app.add_url_rule('/get_relevant_classifications', 'get_relevant_classifications', Classification.get_relevant_classifications, methods=['POST'])

