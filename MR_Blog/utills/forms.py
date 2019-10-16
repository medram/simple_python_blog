from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError, Regexp

from MR_Blog.models import User, Role
from flask_login import current_user



class RegistrationForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9_\-]+$', message='Username must contain only letters numbers or underscore'), length(min=3, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), length(min=4, max=64)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError('This Email is already been used.')

	def validate_username(self, username):
		black_list = ['admin', 'manager', 'administrator', 'author', 'fuck', 'fuck u', 'fuck you', 'owner']
		if username.data.lower() in black_list:
			raise ValidationError('This username is not allowed for use!')

		if User.query.filter_by(username=username.data).first():
			raise ValidationError('This username is already taken. Please choose another one.')



class LoginForm(FlaskForm):

	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')



class UpdateProfileForm(FlaskForm):

	fname = StringField('First name', validators=[DataRequired(), length(min=3, max=15)])
	lname = StringField('Last name', validators=[DataRequired(), length(min=3, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	profile = FileField('Profile image', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
	submit = SubmitField('Update')

	def validate_email(self, email):
		if email.data != current_user.email:
			if User.query.filter_by(email=email.data).first():
				raise ValidationError('This Email is already been used.')


class UpdateUserProfileForm(FlaskForm):

	fname = StringField('First name', validators=[DataRequired(), length(min=3, max=15)])
	lname = StringField('Last name', validators=[DataRequired(), length(min=3, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	profile = FileField('Profile image', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
	status = BooleanField('Active (Not Banned)', validators=[])
	roles = SelectField('Role', validators=[DataRequired()], coerce=int, choices=[role for role in Role.query.with_entities(Role.id, Role.name).all()])
	submit = SubmitField('Update')

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		self.roles.kwargs['default'] = self.user.role.id
		self.status.kwargs['default'] = bool(self.user.status)
		super().__init__(*args, **kwargs)
		

	
	def validate_email(self, email):
		if email.data != self.user.email:
			if User.query.filter_by(email=email.data).first():
				raise ValidationError('This Email is already been used.')
