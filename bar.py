import socket
from datetime import datetime
from flask  import Flask, url_for, request, render_template;
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import time, os

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
db=SQLAlchemy(app)

wsgi_app = app.wsgi_app


#import routes from routes file

from routes import *;
hostname = socket.gethostname()   
IPAddr = socket.gethostbyname(hostname)   
	
	

if __name__ == "__main__":
     
    HOST = os.environ.get('SERVER_HOST' ,IPAddr)
	

    try:
   	PORT =int(os.environ.get('SERVER_PORT' , '3871'))
    except ValueError:
	PORT = 5555
    app.debug = True
    app.run(HOST, PORT)

