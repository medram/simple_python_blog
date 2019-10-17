import os
import hashlib
import secrets
from PIL import Image
from MR_Blog import db
from MR_Blog.models import Setting
from flask_login import current_user
from flask import current_app


def md5(string):
	return hashlib.md5(str(string).encode()).hexdigest()

def sha1(string):
	return hashlib.sha1(str(string).encode()).hexdigest()

def sha256(string):
	return hashlib.sha256(str(string).encode()).hexdigest()


def save_profile_image(fileStorage, user=current_user):
	
	_, f_type = os.path.splitext(fileStorage.filename)
	token_hex = secrets.token_hex(16)
	newFileName = f'{token_hex}{f_type}'
	profiles_folder = os.path.join(current_app.root_path, 'static/imgs/profiles')
	file_path = os.path.join(profiles_folder, newFileName)
	size = (150, 150)

	if os.environ.get('PROFILE_SIZE'):
		size = tuple(int(n) for n in tuple(os.environ.get('PROFILE_SIZE').lower().split('x')))

	try:
		if user.profile_img:
			os.remove(os.path.join(profiles_folder, user.profile_img))
	except IOError:
		pass

	try:
		#fileStorage.save(file_path)
		with Image.open(fileStorage) as i:
			if not i.mode == 'RGB':
				i.convert('RGB')
			i.thumbnail(size)
			i.save(file_path)
		
		user.profile_img = newFileName
		db.session.commit()
	except IOError:
		pass
	return file_path




class Settings:

	settings = {}

	@classmethod
	def load_default_setting(cls):
		# get settings just for the first time.
		if not cls.settings:
			all_options = Setting.query.filter_by(autoload=True).all()
			cls.settings = {option.name:option.value for option in all_options}

	@classmethod
	def get(cls, name, default=None):
		cls.load_default_setting()

		# get this setting value
		if name in cls.settings:
			return cls.settings.get(name, default)
		else:
			opt = Setting.query.filter_by(name=name).first()
			if opt:
				cls.settings[opt.name] = opt.value
				return opt.value
			else:
				return default

def getSetting(name, default=None):
	return Settings.get(name, default)


@current_app.context_processor
def tpl_getSetting():
	''' make detSetting function available into flask templates! '''
	return {'getSetting': getSetting}
