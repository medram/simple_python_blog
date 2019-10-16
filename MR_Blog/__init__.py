import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from MR_Blog.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.root_path = app.config.get('ROOT_PATH')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from MR_Blog import routes





# app.template_folder = os.path.join(app.root_path, 'templates10')
# app.root_path = app.config.get('CORE_PATH')

# app.static_url_path = 'templates10'
# app.static_folder = app.root_path + app.static_url_path