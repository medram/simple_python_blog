from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from MR_Blog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)
	app.root_path = app.config.get('ROOT_PATH')

	# init extentions
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	# within this context we have "current_app" equal to "app" 
	with app.app_context():
		# import Blueprints
		from MR_Blog.dashboard.routes import dashboard 
		from MR_Blog.main.routes import main 
		from MR_Blog.member.routes import member
		from MR_Blog.errors.handlers import errors

		# register Blueprints
		app.register_blueprint(main)
		app.register_blueprint(dashboard)
		app.register_blueprint(member)
		app.register_blueprint(errors)

	return app



# app.template_folder = os.path.join(app.root_path, 'templates10')
# app.root_path = app.config.get('CORE_PATH')

# app.static_url_path = 'templates10'
# app.static_folder = app.root_path + app.static_url_path