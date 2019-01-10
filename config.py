
#All configuration are sttaic for now
import os
import datetime



def getfilepath(filename):
    for file in os.walk(os.getcwd()+"\\static\\"):
        for f in file[2]:
            if f==filename:
                return file[0]
    return os.getcwd()+"\\static\\"
            
DB_PATH = os.path.join(os.path.dirname(__file__), 'temp.db')
SECRET_KEY = 'hjebhjebwhflbkjbfdjbfjlfhdebrhlnbehlbhlerewhherk' 
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DB_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER=os.getcwd()+'\\static\\data\\'
ROOT=os.getcwd()+"\\static\\"
DEBUG = True
admin=1
COOKIE_MAX_AGE=7776000
