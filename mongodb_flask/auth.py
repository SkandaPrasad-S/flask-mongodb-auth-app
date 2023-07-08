import logging
from flask_restx import fields, Namespace, Resource
from flask import request, current_app, Blueprint
from pymongo.errors import DuplicateKeyError
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import BadRequest
import re

bcrypt = Bcrypt()

auth = Namespace('auth', description='Authentication related operations')

user_model = auth.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler for logging
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# Create a formatter and add it to the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

@auth.route('/register')
class UserRegistration(Resource):
    @auth.expect(user_model)
    def post(self):
        # Get the JSON payload
        data = auth.payload
        username = data.get('username')
        password = data.get('password')

        # Validate username and password
        if not username or not password:
            logger.error('Username and password are required.')
            raise BadRequest('Username and password are required.')

        # Validate password length
        if len(password) < 6:
            logger.error('Password should have at least 6 characters.')
            raise BadRequest('Password should have at least 6 characters.')

        # Validate username format to prevent SQL injection
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            logger.error('Invalid username format.')
            raise BadRequest('Invalid username format.')

        # Get the database
        db = current_app.config['DATABASE']
        users_collection = db['users']

        # Check if the user already exists
        if users_collection.find_one({'username': username}):
            logger.error('User already exists.')
            raise BadRequest('User already exists.')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert the new user into the database
        try:
            user = {'username': username, 'password': hashed_password}
            users_collection.insert_one(user)
            logger.info('User registered successfully: %s', username)
            return {'message': 'User registered successfully'}, 201
        except DuplicateKeyError:
            logger.error('User already exists.')
            raise BadRequest('User already exists.')

@auth.route('/login')
class UserLogin(Resource):
    @auth.expect(user_model)
    def post(self):
        # Get the JSON payload
        data = auth.payload
        username = data.get('username')
        password = data.get('password')

        # Validate username and password
        if not username or not password:
            logger.error('Username and password are required.')
            raise BadRequest('Username and password are required.')

        # Get the database
        db = current_app.config['DATABASE']
        users_collection = db['users']

        # Check if the user exists
        user = users_collection.find_one({'username': username})
        if not user:
            logger.error('Invalid credentials for username: %s', username)
            raise BadRequest('Invalid credentials.')

        # Verify the password
        if not bcrypt.check_password_hash(user['password'], password):
            logger.error('Invalid credentials for username: %s', username)
            raise BadRequest('Invalid credentials.')

        # Set the user session or perform any necessary operations
        # For example, you can use Flask's session or a session management library

        logger.info('User authenticated successfully: %s', username)
        return {'message': 'User authenticated successfully'}, 200
