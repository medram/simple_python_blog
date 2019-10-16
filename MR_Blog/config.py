import os

class Config:
	DEBUG = (True if os.environ.get('DEBUG') == 'true' else False)
	SECRET_KEY = os.environ.get('SECRET_KEY')
	# mysql://user:pass@ip:3306/database
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	ROOT_PATH = os.path.join(os.getcwd(), __package__, 'public')