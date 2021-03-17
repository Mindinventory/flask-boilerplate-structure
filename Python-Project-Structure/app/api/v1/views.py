import uuid
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, make_response, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.auth.models import User


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithm="HS256")
            current_user = User.query \
                .filter_by(public_id=data['public_id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


class SignupApiView(Resource):
    def post(self):
        # creates a dictionary of the form data
        data = request.form

        # gets values of data dictionary
        first_name, last_name = data.get('first_name'), data.get('last_name')
        email, password = data.get('email'), data.get('password')

        # checking for existing user
        user = User.query.filter_by(email=email).first()

        if not user:
            # database ORM object
            user = User(
                public_id=str(uuid.uuid4()),
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=generate_password_hash(password)
            )
            # insert user
            db.session.add(user)
            db.session.commit()

            return make_response('Successfully registered.', 201)
        else:
            # returns 202 if user already exists
            return make_response('User already exists. Please Log in.', 202)


class LoginApiView(Resource):
    def post(self):
        # creates dictionary of form data
        auth = request.form

        if not auth or not auth.get('email') or not auth.get('password'):
            # returns 401 if any email or / and password is missing
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
            )

        user = User.query.filter_by(email=auth.get('email')).first()

        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )

        if check_password_hash(user.password, auth.get('password')):
            # generates the JWT Token
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
            # returns 403 if password is wrong
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
        )


@app.route('/test', methods=['GET'])
@token_required
def test(current_user):
    return jsonify({'user': current_user.first_name})



