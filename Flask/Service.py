import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
from Models.User_Model import User_Model
from Models.Service_Model import Service_Model, User_Subscription, Device_Subscription, Enum, Enum_Entry
from Models.Device_Model import Device_Model, User_Device

class Service():

    @staticmethod
    def list_all_services():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            if User_Model.query.filter_by(name = auth.username).first().account_type == "admin":
                services = Service_Model.query.all()
                return_json_list = []
                for report in services:
                    dict_local = {'name': report.name}
                    return_json_list.append(dict_local)
                return_string = json.dumps(return_json_list, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            else:
                dict_local = {'code': 37, 'message': "Permission error " + str(auth.username)}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            dict_local = {'code': 31, 'message': "auth error "}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def add_service():
        if User_Model.authenticate_user(request.authorization):
            parsed_json = request.get_json()
            service_name = parsed_json["service_name"]
            if not Service_Model.query.filter_by(name = service_name).scalar():
                new_service = Service_Model(service_name)
                db.session.add(new_service)

                attributes = parsed_json["attributes"]
                for att_key in attributes.keys():
                    enum_id = str(uuid.uuid4())
                    _enum = Enum(enum_id, att_key, service_name)
                    for val in attributes[att_key]:
                        entry_id = str(uuid.uuid4())
                        enum_val = Enum_Entry(entry_id, val, enum_id)
                        db.session.add(enum_val)
                    db.session.add(_enum)
                db.session.commit()
                return_json = {'code': 200}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                print("[DEBUG] - list_device_events: Successful")
                return return_string    
            else:
                #ColorPrint.print_message("Debug", "register_account_user", "email already exists")
                return_json = {'code': 31, 'message': "Service already exists."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "list_device_events", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication error"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def remove_service():
        if User_Model.authenticate_user(request.authorization):
            parsed_json = request.get_json()
            service_name = parsed_json["name"]
            service = Service_Model.query.filter_by(name = service_name).first()
            if service:
                db.session.delete(service)
                db.session.commit()
                return_json = { 'code' : 200 }
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                print("[DEBUG] - list_device_events: Successful")
                return return_string    
            else:
                #ColorPrint.print_message("Debug", "register_account_user", "email already exists")
                return_json = {'code': 31, 'message': "Service doesn't exist anyways."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "list_device_events", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication error"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

#!!!!!! SERVICE ATTRIBUTES !!!!!!!

    @staticmethod
    def add_service_attributes():
        if User_Model.authenticate_user(request.authorization):
            parsed_json = request.get_json()
            service_name = parsed_json["service_name"]
            service = Service_Model.query.filter_by(name = service_name).first()
            if service:
                enums = Enum.query.join(Service_Model).filter(Service_Model.name == service_name).all()
                attributes = parsed_json["attributes"]
                for att_key in attributes.keys():
                    for enum in enums:
                        #case where it already exists
                        if enum.name == att_key:
                            db.session.delete(enum)
                    enum_id = str(uuid.uuid4())
                    _enum = Enum(enum_id, att_key, service_name)
                    for val in attributes[att_key]:
                        entry_id = str(uuid.uuid4())
                        enum_val = Enum_Entry(entry_id, val, enum_id)
                        db.session.add(enum_val)
                    db.session.add(_enum)
                db.session.commit()
                return_json = { 'code' : 200 }
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                print("[DEBUG] - remove_service_attributes: Successful")
                return return_string    
            else:
                #ColorPrint.print_message("Debug", "register_account_user", "email already exists")
                return_json = {'code': 31, 'message': "Service doesn't exist anyways."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "remove_service_attributes", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication error"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def remove_service_attributes():
        if User_Model.authenticate_user(request.authorization):
            parsed_json = request.get_json()
            service_name = parsed_json["service_name"]
            service = Service_Model.query.filter_by(name = service_name).first()
            if service:
                enums = Enum.query.join(Service_Model).filter(Service_Model.name == service_name).all()
                attributes = parsed_json["attributes"]
                for att_key in attributes:
                    for enum in enums:
                        if enum.name == att_key:
                            db.session.delete(enum)
                db.session.commit()
                return_json = { 'code' : 200 }
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                print("[DEBUG] - remove_service_attributes: Successful")
                return return_string    
            else:
                #ColorPrint.print_message("Debug", "register_account_user", "email already exists")
                return_json = {'code': 31, 'message': "Service doesn't exist anyways."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "remove_service_attributes", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication error"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def get_services_attributes():
        if User_Model.authenticate_user(request.authorization):
            parsed_json = request.get_json()
            service_names = parsed_json["service_names"]
            return_dict = {}
            for s_name in service_names:
                return_dict[s_name] = {}
            enums = Enum.query.join(Service_Model).filter(Service_Model.name.in_(service_names)).all()
            for enum in enums:
                enum_entries = Enum_Entry.query.join(Enum).filter(Enum.id == enum.id).all()
                return_dict[enum.service_name][enum.name] = []
                for enum_entry in enum_entries:
                    return_dict[enum.service_name][enum.name] += [enum_entry.value]
            return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
            print("[DEBUG] - remove_service_attributes: Successful")
            return return_string    
        else:
            ColorPrint.print_message("Warning", "remove_service_attributes", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication error"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

#DEVICE SHIT!!!!!!!!!!!!!!!!!!

    @staticmethod
    def get_device_services():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()
            device_id = parsed_json["device_id"]
            if User_Device.query.filter_by(device_id = device_id, user_name = user_id).scalar():
                #then this device is owned by this user so we're good
                subscriptions = Device_Subscription.query.filter_by(device_id = device_id).all()
                ColorPrint.print_message("Warning", "get_device_services", "sub: " + str(subscriptions))
                array_local = []
                for sub in subscriptions:
                    array_local += [sub.service_name]
                return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
                ColorPrint.print_message("Debug", "list_user_devices", "Success")
                return return_string
            else:
                ColorPrint.print_message("Warning", "list_user_devices", "User does not have access to this device.")
                dict_local = {'code': 31, 'message': "User does not have access to device."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "list_user_devices", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def add_device_service():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()
            device_id = parsed_json["device_id"]
            if User_Device.query.filter(User_Device.device_id == device_id, User_Device.user_name == user_id).scalar():
                #this means that it doesn't exist yet and we can add it
                service_name = parsed_json["service_name"]
                device_subscription = Device_Subscription.query.filter(Device_Subscription.device_id == device_id, Device_Subscription.service_name == service_name).first()
                if not device_subscription:
                    new_sub = Device_Subscription(device_id, service_name)
                    db.session.add(new_sub)
                    db.session.commit()
                    return_json = {'code': 200}
                    return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                    return return_string
                else:
                    return_json = {'code': 200, 'message': "Device is already subscribing."}
                    return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                    return return_string
            else:
                return_json = {'code': 31, 'message': "User does not have access to device."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "list_user_devices", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def remove_device_service():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()
            device_id = parsed_json["device_id"]
            if User_Device.query.filter(User_Device.device_id == device_id, User_Device.user_name == user_id).scalar():
                #this means that it doesn't exist yet and we can add it
                service_name = parsed_json["service_name"]
                device_subscription = Device_Subscription.query.filter(Device_Subscription.device_id == device_id, Device_Subscription.service_name == service_name).first()
                if device_subscription:
                    db.session.delete(device_subscription)
                    db.session.commit()
                    return_json = {'code': 200}
                    return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                    return return_string
                else:
                    return_json = {'code': 200, 'message': "Device subscription doesn't exist anyways."}
                    return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                    return return_string
            else:
                return_json = {'code': 31, 'message': "User does not have access to device."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "list_user_devices", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

#USER SHIT!!!!!!!!!!!!!!!!!!

    @staticmethod
    def get_user_services():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()

            subscriptions = User_Subscription.query.filter_by(user_name = user_id).all()
            array_local = []
            for sub in subscriptions:
                array_local += [sub.service_name]
            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            ColorPrint.print_message("Debug", "get_user_services", "Success")
            return return_string
        else:
            ColorPrint.print_message("Warning", "get_user_services", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def add_user_service():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()
            service_name = parsed_json["name"]
            if not User_Subscription.query.filter(User_Subscription.user_name == user_id, User_Subscription.service_name == service_name).first():
                #this means that it doesn't exist yet and we can add it
                service = Service_Model.query.filter_by(name = service_name).first()
                new_sub = User_Subscription(user_id, service.name)
                db.session.add(new_sub)
                db.session.commit()
                return_json = {'code': 200}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            else:
                return_json = {'code': 31, 'message': "User is already subscribing."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "list_user_devices", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def remove_user_service():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()
            service_name = parsed_json["name"]
            user_subscription = User_Subscription.query.filter(User_Subscription.user_name == user_id, User_Subscription.service_name == service_name).first()
            if user_subscription:
                db.session.delete(user_subscription)
                db.session.commit()
                return_json = {'code': 200}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            else:
                return_json = {'code': 31, 'message': "The service subscription already didn't exist."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "remove_user_service", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string



app.add_url_rule('/list_all_services', 'list_all_services', Service.list_all_services, methods=['GET'])
app.add_url_rule('/add_service', 'add_service', Service.add_service, methods=['POST'])
app.add_url_rule('/remove_service', 'remove_service', Service.remove_service, methods=['POST'])

app.add_url_rule('/add_service_attributes', 'add_service_attributes', Service.add_service_attributes, methods=['POST'])
app.add_url_rule('/remove_service_attributes', 'remove_service_attributes', Service.remove_service_attributes, methods=['POST'])
app.add_url_rule('/get_services_attributes', 'get_services_attributes', Service.get_services_attributes, methods=['POST'])

app.add_url_rule('/get_device_services', 'get_device_services', Service.get_device_services, methods=['POST'])
app.add_url_rule('/add_device_service', 'add_device_service', Service.add_device_service, methods=['POST'])
app.add_url_rule('/remove_device_service', 'remove_device_service', Service.remove_device_service, methods=['POST'])

app.add_url_rule('/get_user_services', 'get_user_services', Service.get_user_services, methods=['GET'])
app.add_url_rule('/add_user_service', 'add_user_service', Service.add_user_service, methods=['POST'])
app.add_url_rule('/remove_user_service', 'remove_user_service', Service.remove_user_service, methods=['POST'])

