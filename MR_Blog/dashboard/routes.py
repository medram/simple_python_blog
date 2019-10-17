from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required

from MR_Blog import db
from MR_Blog.models import User
from MR_Blog.utills import common
from MR_Blog.dashboard import forms


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@login_required
def index():
	user = current_user
	return render_template('dashboard/index.html', user=user, page_title='Dashboard')



@dashboard.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
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
		return redirect(url_for('dashboard.profile'))

	elif request.method == 'GET':
		form.fname.data = user.fname
		form.lname.data = user.lname
		form.email.data = user.email

	return render_template('dashboard/profile.html', user=user, form=form, page_title='Profile')



@dashboard.route('/posts')
@login_required
def posts():
	pass



@dashboard.route('/users')
@login_required
def users():
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



@dashboard.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def user(user_id):
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
		return redirect(url_for('dashboard.user', user_id=user_to_edit.id))

	elif request.method == 'GET':
		form.fname.data = user_to_edit.fname
		form.lname.data = user_to_edit.lname
		form.email.data = user_to_edit.email

	return render_template('dashboard/user_edit.html', user=user, form=form, user_to_edit=user_to_edit, page_title='Edit User')




@dashboard.route('/settings')
@login_required
def settings():
	pass