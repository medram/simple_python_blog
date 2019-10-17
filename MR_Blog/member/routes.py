from flask import Blueprint, render_template
from flask_login import current_user, login_required

member = Blueprint('member', __name__, url_prefix='/member')

@member.route('/')
@login_required
def account():
	user = current_user
	return render_template('dashboard/index.html', user=user)
