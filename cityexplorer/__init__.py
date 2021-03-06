from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_mail import Mail
from cityexplorer.config import Config

app = Flask(__name__)

app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MONGO_URI'] = Config.MONGO_URI
mail = Mail(app)
mongo = PyMongo(app)

from cityexplorer import routes
