from functools import wraps
from flask import request, Response
from sql_queries import sql_queries


class UserAuthentication():
    #TODO add account permission check
    #TODO implement logger
    #TODO protect against brute forcing
    #TODO refactor

    @staticmethod
    def check_auth(username, password):
        """This function is called to check if a username /
        password combination is valid.
        """
        db_password = sql_queries.get_user_password(username)

        if db_password is not None:
            if db_password == password:
                return True
            else:
                #ColorPrint.print_message("Warning", "authenticate_user", "User Authentication Failed, Wrong password")
                return False
        else:
            #ColorPrint.print_message("Warning", "authenticate_user", "User Authentication Failed, non existent user " + username + " " + password + " " + db_password)
            return False

    @staticmethod
    def authenticate():
        """Sends a 401 response that enables basic auth"""
        return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    @staticmethod
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            auth = request.authorization
            if not auth or not UserAuthentication.check_auth(auth.username, auth.password):
                return UserAuthentication.authenticate()
            return f(*args, **kwargs)
        return decorated


class DeviceAuthentication():

    @staticmethod
    def check_auth(username, password):
        """This function is called to check if a username /
        password combination is valid.
        """
        return username == 'admin' and password == 'secret'

    @staticmethod
    def authenticate():
        """Sends a 401 response that enables basic auth"""
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

    @staticmethod
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not DeviceAuthentication.check_auth(auth.username, auth.password):
                return DeviceAuthentication.authenticate()
            return f(*args, **kwargs)

        return decorated
