from flask import abort
from flask_login import current_user

def roles_required(*args, **kwargs):
	# user = current_user
	# print('>>>> user: ', user)
	def wrapper(func):
		# if 'user' in kwargs.keys():
		# 	user = kwargs.get('user')
		# 	for role in args:
		# 		if user.role.name == role:
		# 			return func

		return func
		return lambda: abort(403)
	return wrapper