from datetime import datetime

from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user

from MR_Blog import db, bcrypt
from MR_Blog.models import User, Post
from MR_Blog.utills import common
from MR_Blog.main import forms


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
	posts = Post.query.all()
	return render_template('home.html', posts=posts)


@main.route('/about')
def about():
	return render_template('about.html', title="About us")


@main.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('member.account'))
	
	form = forms.RegistrationForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password, token=common.sha1(datetime.utcnow()), role_id=4)		
		db.session.add(user)
		db.session.commit()
	
		flash(f"Your account has been created!, You can log in now.", 'success')
		return redirect(url_for('main.login'))

	return render_template('register.html', form=form, title='Sign Up')



@main.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('member.account'))

	form = forms.LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			#flash(f"You have logged in suucessfully.", 'success')
			nextURL = request.args.get('next')
			return redirect(nextURL) if nextURL else redirect(url_for('member.account'))
		else:
			flash(f"Incorrect email or password!", 'warning')

	return render_template('login.html', form=form, title='Login')



@main.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))
