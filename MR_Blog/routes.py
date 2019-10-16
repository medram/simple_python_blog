from datetime import datetime

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required

from MR_Blog import app, db, bcrypt
from MR_Blog.models import User, Post
from MR_Blog.utills import forms, common

import MR_Blog.middlewares as mdl





@app.route('/')
@app.route('/home')
def home():
	posts = Post.query.all()
	return render_template('home.html', posts=posts)


@app.route('/about')
def about():
	return render_template('about.html', title="About us")


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	
	form = forms.RegistrationForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password, token=common.sha1(datetime.utcnow()), role_id=4)		
		db.session.add(user)
		db.session.commit()
	
		flash(f"Your account has been created!, You can log in now.", 'success')
		return redirect(url_for('login'))

	return render_template('register.html', form=form, title='Sign Up')



@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account'))

	form = forms.LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			#flash(f"You have logged in suucessfully.", 'success')
			nextURL = request.args.get('next')
			return redirect(nextURL) if nextURL else redirect(url_for('account'))
		else:
			flash(f"Incorrect email or password!", 'warning')

	return render_template('login.html', form=form, title='Login')



@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
	user = current_user
	return render_template('dashboard/index.html', user=user)


@app.route('/dashboard')
#@mdl.roles_required('admin')
@login_required
def dashboard():
	user = current_user
	return render_template('dashboard/index.html', user=user, page_title='Dashboard')



@app.route('/dashboard/profile', methods=['GET', 'POST'])
@login_required
def dashboard_profile():
	user = current_user
	form = forms.UpdateProfileForm()

	if form.validate_on_submit():
		if form.profile.data:
			common.save_profile_image(form.profile.data)

		user.fname = form.fname.data
		user.lname = form.lname.data
		user.email = form.email.data
		
		db.session.commit()
		flash('Updated successfully.', 'success')
		return redirect(url_for('dashboard_profile'))

	elif request.method == 'GET':
		form.fname.data = user.fname
		form.lname.data = user.lname
		form.email.data = user.email

	return render_template('dashboard/profile.html', user=user, form=form, page_title='Profile')



@app.route('/dashboard/posts')
@login_required
def dashboard_posts():
	pass



@app.route('/dashboard/users')
@login_required
def dashboard_users():
	user = current_user
	search = request.args.get('users_search')
	page = request.args.get('page', 1, type=int)
	per_page = 20
	
	if search:
		if search.startswith('@'):
			users = User.query.filter(User.username.like('%' + search[1:] + '%')).order_by(User.created.desc()).paginate(page, per_page, error_out=False)
		else:
			users = User.query.filter(User.username.like('%' + search + '%') | User.email.like('%' + search + '%') | User.fname.like('%' + search + '%') | User.lname.like('%' + search + '%')).order_by(User.created.desc()).paginate(page, per_page, error_out=False)
	else:
		users = User.query.order_by(User.created.desc()).paginate(page, per_page, error_out=False)

	# exclode current user file results
	users.items = [user for user in users.items if user.id != current_user.id]

	return render_template('dashboard/users.html', user=user, page_title='Users', users=users)



@app.route('/dashboard/user/<int:user_id>/edit', methods=['GET', 'POST'])
def dashboard_user(user_id):
	user = current_user
	user_to_edit = User.query.filter_by(id=user_id).first()
	form = forms.UpdateUserProfileForm(user=user_to_edit)

	if not user_to_edit:
		return render_template('dashboard/user_edit.html', user=user, page_title='Edit User', form=form, message=f'The User ({user_id}) is not Found.')

	if form.validate_on_submit():
		if form.profile.data:
			common.save_profile_image(form.profile.data, user=user_to_edit)

		user_to_edit.fname = form.fname.data
		user_to_edit.lname = form.lname.data
		user_to_edit.email = form.email.data
		user_to_edit.status = int(form.status.data)
		user_to_edit.role_id = int(form.roles.data)

		db.session.commit()
		flash('Updated successfully.', 'success')
		return redirect(url_for('dashboard_user', user_id=user_to_edit.id))

	elif request.method == 'GET':
		form.fname.data = user_to_edit.fname
		form.lname.data = user_to_edit.lname
		form.email.data = user_to_edit.email

	return render_template('dashboard/user_edit.html', user=user, form=form, user_to_edit=user_to_edit, page_title='Edit User')




@app.route('/dashboard/settings')
@login_required
def dashboard_settings():
	pass