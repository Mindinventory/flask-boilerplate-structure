from flask import Blueprint
from flask_restful import Api

from app.api.v1.views import SignupApiView, LoginApiView

api = Blueprint('api', __name__, url_prefix='/api/')
rest_api = Api(api)

rest_api.add_resource(SignupApiView, '/auth/signup')
rest_api.add_resource(LoginApiView, '/auth/login')