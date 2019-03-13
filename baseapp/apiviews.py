from baseapp import app
from werkzeug.security import check_password_hash
from baseapp.models import Users
from baseapp.controllers import UsersController
from flask import render_template, request, redirect, url_for, jsonify, make_response
import jwt
import datetime
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Users.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/api/login')
def apilogin():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = Users.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'username' : user.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@app.route('/api/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}), 401

    users = Users.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        user_data['email'] = user.email
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/api/user/<int:user_id>', methods=['GET'])
@token_required
def get_one_user(current_user, user_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}), 401

    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'}), 404

    user_data = {}
    user_data['id'] = user.id
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    user_data['email'] = user.email

    return jsonify({'user' : user_data})

@app.route('/api/user', methods=['POST','PUT','DELETE'])
@token_required
def crud_user(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}), 401

    data = request.get_json()
    userc = UsersController()
    if request.method == 'POST':
        if userc.add(data):
            return jsonify({'message' : 'New user created!'})

        return jsonify({'message' : 'failed to create user!'})

    if request.method == 'PUT':
        if userc.edit(data):
            return jsonify({'message' : 'User modified'})

        return jsonify({'message' : 'failed to modify user!'})

    if request.method == 'DELETE':
        if userc.delete(data):
            return jsonify({'message' : 'User deleted'})

        return jsonify({'message' : 'failed to delete user!'})

