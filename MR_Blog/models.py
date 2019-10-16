import os

from datetime import datetime
from MR_Blog import db, login_manager, app
from flask_login import UserMixin
from flask import url_for, Markup

class Comment(db.Model):

	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	status = db.Column(db.Integer, default=1)
	updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	created = db.Column(db.DateTime, default=datetime.utcnow)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
	parent_comm = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)

	getSubComments = db.relationship('Comment', remote_side='Comment.id', backref=db.backref('getParentComment', lazy=True))

	def __repr__(self):
		return f"<Comment (id={self.id})>"


@login_manager.user_loader
def load(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):

	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(25))
	lname = db.Column(db.String(25))
	username = db.Column(db.String(25), unique=False, nullable=False)
	email = db.Column(db.String(180), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	token = db.Column(db.String(40), unique=True, nullable=False)
	status = db.Column(db.Integer, default=1)
	profile_img = db.Column(db.String(40))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
	updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	created = db.Column(db.DateTime, default=datetime.utcnow)

	posts = db.relationship('Post', backref='getUser', lazy=True)
	comments = db.relationship('Comment', backref=db.backref('getUser', lazy=True))

	def getProfileImg(self):
		default_profile = 'default.png'
		#profileURI = os.path.join(app.static_url_path, 'imgs/profiles', self.profile_img if self.profile_img else default_profile)
		profileURI = url_for('static', filename=f'imgs/profiles/{(self.profile_img if self.profile_img else default_profile)}')
		return profileURI

	def getBadge(self):
		colors = {'author': 'aqua', 'owner': 'green', 'admin': 'yellow'}
		color = None
		try:
			color = colors[self.role.name]
		except:
			pass
		return Markup(f'<span class="badge bg-{color}">{self.role.name}</span>')

	def __repr__(self):
		return f"<User (id={self.id})>"


Post_category = db.Table('post_category',
		db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True,),
		db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
	)

class Post(db.Model):

	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(180), nullable=False)
	slug = db.Column(db.String(180), unique=True, nullable=False)
	content = db.Column(db.Text)
	status = db.Column(db.Integer, default=1)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	created = db.Column(db.DateTime, default=datetime.utcnow)

	comments = db.relationship('Comment', backref=db.backref('getPost', lazy=True))
	categories = db.relationship('Category', secondary=Post_category, lazy='subquery', backref=db.backref('getPosts', lazy=True))

	def __repr__(self):
		return f"<Post (id={self.id})>"


role_perm = db.Table('role_perm', 
		db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
		db.Column('parm_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
	)

class Role(db.Model):

	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	
	users = db.relationship('User', backref='role', lazy=True)
	permissions = db.relationship('Permission', secondary=role_perm, lazy='subquery', backref=db.backref('roles', lazy=True))

	def __repr__(self):
		return f"<Role (id={self.id}, name={self.name})>"

@db.event.listens_for(Role.__table__, 'after_create')
def roles_insert_initiale_values(*args, **kwargs):
	db.session.add(Role(name='owner'))
	db.session.add(Role(name='admin'))
	db.session.add(Role(name='author'))
	db.session.add(Role(name='other'))
	db.session.commit()

#db.event.listen(Role.__table__, 'after_create', roles_insert_initiale_values)

class Permission(db.Model):

	__tablename__ = 'permissions'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)

	def __repr__(self):
		return f"<Permission (id={self.id}, name={self.name})>"




# class Role_perm(db.Model):

# 	__tablename__ = 'role_perm'
# 	id = db.Column(db.Integer, primary_key=True)
# 	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
# 	perm_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)

# 	def __repr__(self):
# 		return f"<Role_perm (role_id={self.role_id}, perm_id={self.perm_id})>"


class Category(db.Model):

	__tablename__ = 'categories'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	slug = db.Column(db.String(180), unique=True, nullable=False)
	parent_cat = db.Column(db.Integer, db.ForeignKey('categories.id'))

	getSubCategories = db.relationship('Category', remote_side='Category.id', backref=db.backref('getParentCategory', lazy=True))

	def __repr__(self):
		return f"<Category (id={self.id}, name={self.name})>"

# class Post_category(db.Model):

# 	__tablename__ = 'post_category'
# 	id = db.Column(db.Integer, primary_key=True)
# 	post_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
# 	category_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)

# 	def __repr__(self):
# 		return f"<Post_category (post_id={self.post_id}, category_id={self.category_id})>"


class Page(db.Model):

	__tablename__ = 'pages'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(180), nullable=False)
	slug = db.Column(db.String(180), unique=True, nullable=False)
	status = db.Column(db.Integer, default=1)
	updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	created = db.Column(db.DateTime, default=datetime.utcnow)


	def __repr__(self):
		return f"<Page (id={self.id})>"


class Setting(db.Model):

	__tablename__ = 'settings'
	name = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
	value = db.Column(db.String(64))
	autoload = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return f"<Setting ({self.name})>"


@db.event.listens_for(Setting.__table__, 'after_create')
def init_settings(*args, **kwargs):
	db.session.add(Setting(name='sitename', value='MRBlog', autoload=True))
	db.session.add(Setting(name='default_timezone', value='Africa/Casablanca', autoload=True))
	db.session.add(Setting(name='powredby', value='MR4Web.com', autoload=True))
	db.session.add(Setting(name='date_format', value='d-m-Y H:i', autoload=True))
	db.session.add(Setting(name='shutdown', value='1', autoload=True))
	db.session.add(Setting(name='shutdown_msg', value='The site was closed now, please try later soon.', autoload=True))
	db.session.commit()
