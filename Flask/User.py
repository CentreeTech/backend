import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime
from Models.Service_Model import Service_Model, User_Subscription
from Models.User_Model import User_Model

class User():

    @staticmethod
    def login():
        #TODO add non existent user handling
        parsed_json = request.get_json()
        email = parsed_json["email"]
        password = parsed_json["password"]

        user = User_Model.query.filter_by(email = email).first();

        if password == user.password:
            dict_local = {'name': user.name, 'created_at': str(user.created_at), 'email': user.email, 'password': user.password}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string
        else:
            dict_local = {'code': 31, 'message': "login failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def list_all_users():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            if User_Model.query.filter_by(name = auth.username).first().account_type == "admin":
                db_user_devices = User_Model.query.all()
                return_json_list = []
                for report in db_user_devices:
                    dict_local = {'name': report.name,
                                    'email': report.email,
                                    'password' : report.password,
                                    'created_at': str(report.created_at),
                                    'account_type': report.account_type}

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
    def register_account_user():
        if User_Model.authenticate_user(request.authorization):
            parsed_json = request.get_json()
            email = parsed_json["email"]
            password = parsed_json["password"]
            # Test this shit for syntax
            if not User_Model.query.filter_by(email = email).first():
                print("[DEBUG] - registerAccount: Registering User")
                print("email " + parsed_json["email"])
                # Random name for the account
                name = str(uuid.uuid4())
                # Execute Add user sql query
                new_user = User_Model(name = name, password = password, email = email, account_type = 'user')
                db.session.add(new_user)
                db.session.commit()
                # Set Headers for http reply
                return_json = {'code': 200}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
                # print "[DEBUG] - registerAccount: Account registered for "
                #ColorPrint.print_message("Debug", "register_account_user", "user registration successful")
            else:
                #ColorPrint.print_message("Debug", "register_account_user", "email already exists")
                return_json = {'code': 31, 'message': "email already in use"}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            #ColorPrint.print_message("Error", "register_account_user", "User Registration Failed")
            return_json = {'code': 31, 'message': "bad login; account registration failed"}
            return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string


    @staticmethod
    def get_user_subscriptions():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            user_subscriptions = User_Subscription.query.filter(User_Subscription.user_name == user_id).all()
            array_local = []
            for report in user_subscriptions:
                array_local += [report.service_name]
            return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
            ColorPrint.print_message("Debug", "list_user_devices", "Success")
            return return_string
        else:
            ColorPrint.print_message("Warning", "list_user_devices", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def add_user_subscription():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()
            service_name = parsed_json["service"]

            if not Service_Model.query.filter_by(name = service_name).first():
                return_json = {'code': 31, 'message': "Service doesn't exist."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            if not User_Subscription.query.filter(User_Subscription.user_name == user_id, User_Subscription.service_name == service_name).first(): #if this subscription does not exist
                #this means that it doesn't exist yet and we can add it
                ColorPrint.print_message("Debug", "list_user_devices", "Got this far...")
                user = User_Model.query.filter(User_Model.name == user_id).first()
                service = Service_Model.query.filter(Service_Model.name == service_name).first()
                subscription = User_Subscription(user, service)
                db.session.add(subscription)
                db.session.commit()
                return_json = {'code': 200}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            else:
                return_json = {'code': 31, 'message': "User already subscribed."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "list_user_devices", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

    @staticmethod
    def remove_user_subscription():
        if User_Model.authenticate_user(request.authorization):
            auth = request.authorization
            user_id = auth.username
            parsed_json = request.get_json()
            service_name = parsed_json["service"]
            service = User_Subscription.query.filter(User_Subscription.user_name == user_id, User_Subscription.service_name == service_name).first()
            if service: #if this subscription does exist
                #go ahead and remove it.
                db.session.delete(service)
                db.session.commit()
                return_json = {'code': 200}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
            else:
                return_json = {'code': 31, 'message': "Subscription already didn't exist."}
                return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
                return return_string
        else:
            ColorPrint.print_message("Warning", "list_user_devices", "User Authentication Failed")
            dict_local = {'code': 31, 'message': "user authentication failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Addding the URL rules

app.add_url_rule('/login', 'login', User.login, methods=['POST'])
app.add_url_rule('/list_all_users', 'list_all_users', User.list_all_users, methods=['GET'])
app.add_url_rule('/register_account_user', 'register_account_user', User.register_account_user, methods=['POST'])
app.add_url_rule('/get_user_subscriptions', 'get_user_subscriptions', User.get_user_subscriptions, methods=['GET'])
app.add_url_rule('/add_user_subscription', 'add_user_subscription', User.add_user_subscription, methods=['POST'])
app.add_url_rule('/remove_user_subscription', 'remove_user_subscription', User.remove_user_subscription, methods=['POST'])
