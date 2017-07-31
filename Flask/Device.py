import sys
import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint

from Models.Service_Model import Device_Subscription
from Models.User_Model import User_Model
from Models.Device_Model import Device_Model, User_Device

class Device():

    @staticmethod
    def register_device():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            try:
                # print "[DEBUG] - registerAccount:"
                parsed_json = request.get_json()
                id = parsed_json["id"]
                name = parsed_json["name"]
                password = parsed_json["password"]
                # owner = parsedJson["owner"]
                software_version = parsed_json["software_version"]
                location = parsed_json["location"]
                if not Device_Model.query.filter_by(id = id).scalar() and User_Model.query.filter_by(name = user_id).scalar():
                    print("[DEBUG] - register_device: Registering Device")
                    print("id " + parsed_json["id"])
                    try:
                        new_device = Device_Model(id = id, password = password, owner = user_id, software_version = software_version, location = location, name = name)
                        db.session.add(new_device)
                        db.session.commit()

                        return_json = {'code': 200}
                        return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))

                        # needs to be json reply
                        print("[DEBUG] - register_device: Device registered")
                        return return_string
                    except:
                         raise
                         ColorPrint.print_message("Error", "register_device", " Database Commit Failed")
                         return_json = {'code': 31, 'message': "Internal database error"}
                         return json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                else:
                    ColorPrint.print_message("Warning", "register_device", "Owner or device existence problem")

                    return_json = {'code': 31, 'message': "Error Device exists or owner doesn't exists"}
                    return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                    return return_string

            except KeyError:
                ColorPrint.print_message("Error", "register_device", "Missing a Key")
                return_json = {'code': 400, 'message': "Missing a key"}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:

            return_json = {'code': 31, 'message': "Auth failed"}
            return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def list_all_devices():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            if User_Model.query.filter_by(name = user_id).first().account_type == "admin":
                db_all_devices = Device_Model.query.all()
                return_json_list = []
                for report in db_all_devices:

                    dict_local = {'software_version': str(report.software_version),
                                  'location': report.location,
                                  'name' : report.name}

                    return_json_list.append({report.id : dict_local})

                return_string = json.dumps(return_json_list, sort_keys=True, indent=4, separators=(',', ': '))
                print("[DEBUG] - list_all_devices: Successful")
                return return_string

            else:
                # print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- list_all_devices: Restricted Access"
                ColorPrint.print_message("Warning", "list_all_devices", "Permission Denied")
                dict_local = {'code': 37, 'message': "Permission error"}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))

                return return_string
        else:
            # print bcolors.FAIL + "[ERROR]" + bcolors.ENDC + "- list_all_devices: Auth failed"
            ColorPrint.print_message("Warning", "list_all_devices", "Authentication Failed")

            dict_local = {'code': 31, 'message': "auth error"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))

            return return_string

    @staticmethod
    def list_user_devices():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            user_devices = Device_Model.query.filter(Device_Model.owners.any(user_name = user_id)).all()
            return_json_dict = {}
            for report in user_devices:
                dict_local = {'software_version': str(report.software_version),
                              'location': report.location,
                              'name' : report.name}
                return_json_dict[report.id] = dict_local

            return_string = json.dumps(return_json_dict, sort_keys=True, indent=4, separators=(',', ': '))
            ColorPrint.print_message("Debug", "list_user_devices", "Success")
            return return_string

        else:
            ColorPrint.print_message("Warning", "list_user_devices", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))

            return return_string

    @staticmethod
    def add_user_device():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()
            device_id = parsed_json["device_id"]
            user_devices = User_Device.query.filter(User_Device.user_name == user_id, User_Device.device_id == device_id).first()
            if not user_devices:
                user_device = User_Device(user_id, device_id)
                db.session.add(user_device)
                db.session.commit()
                dict_local = {'code': 200}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                ColorPrint.print_message("Debug", "list_user_devices", "Success")
                return return_string
            else:
                ColorPrint.print_message("Warning", "add_user_device", "Subscription already exists.")
                dict_local = {'code': 200, 'message': "Subscription already exists."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "list_user_devices", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def remove_user_device():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()
            device_id = parsed_json["device_id"]
            user_device = User_Device.query.filter(User_Device.user_name == user_id, User_Device.device_id == device_id).first()
            if user_device:
                db.session.delete(user_device)
                db.session.commit()
                dict_local = {'code': 200}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                ColorPrint.print_message("Debug", "remove_user_device", "Success")
                return return_string
            else:
                ColorPrint.print_message("Warning", "add_user_device", "Subscription already exists.")
                dict_local = {'code': 200, 'message': "Subscription already exists."}
                return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "remove_user_device", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

app.add_url_rule('/add_user_device', 'add_user_device', Device.add_user_device, methods=['POST'])
app.add_url_rule('/remove_user_device', 'remove_user_device', Device.remove_user_device, methods=['POST'])
app.add_url_rule('/register_device', 'register_device', Device.register_device, methods=['POST'])
app.add_url_rule('/list_user_devices', 'list_user_devices', Device.list_user_devices, methods=['GET'])
app.add_url_rule('/list_all_devices', 'list_all_devices', Device.list_all_devices, methods=['GET'])
