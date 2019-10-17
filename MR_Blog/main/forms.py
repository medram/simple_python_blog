from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError, Regexp

from MR_Blog.models import User



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