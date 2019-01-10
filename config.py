
#All configuration are sttaic for now
import os
import datetime


DB_PATH = os.path.join(os.path.dirname(__file__), 'temp.db')
SECRET_KEY = 'hjebhjebwhflbkjbfdjbfjlfhdebrhlnbehlbhlerewhherk' 
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DB_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER=os.getcwd()+'\\static\\data\\'
ROOT=os.getcwd()+"\\static\\"
DEBUG = True
admin=1
COOKIE_MAX_AGE=7776000