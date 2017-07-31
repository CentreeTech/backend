from flask import Flask
from flask import request

#from authentication import UserAuthentication
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask('Flask Application')

# app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../../file_storage/'
app.config['Test'] = "Test confirmed"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ubuntu:elephants_remember_1984@localhost/centree'
CORS(app)
db = SQLAlchemy(app)
