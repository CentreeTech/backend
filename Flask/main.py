from flask import Flask
from flask import request, send_from_directory

#from authentication import UserAuthentication
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flaskapp import app, db

from User import User
from Device import Device
from Event import Event
from Service import Service
from Cloud_Storage import Cloud_Storage
from Classification import Classification
from Generate import Generate

#db.drop_all()
db.create_all()


@app.route('/mapui')
def serve_mapui():
    return send_from_directory('../../centree_webapp/build/', 'server.js')

@app.route('/classui')
def serve_classui():
    return send_from_directory('../client/classify_redux/build/', 'server.js')

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)
