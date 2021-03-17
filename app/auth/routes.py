from flask import Blueprint

from app import app
from app.auth.views import *

auth = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/', methods=['GET'])
def index():
    return index_view()


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    return signup_view()


@auth.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token):
    return confirm_view(token)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return login_view()


@auth.route('/logout')
def logout():
    return logout_view()


@auth.route('/account')
def account():
    return account_view()


@auth.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return forgot_view()


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    return reset_view(token)
