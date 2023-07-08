import pytest
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restx import Api
from pymongo import MongoClient
from mongodb_flask.auth import UserRegistration, UserLogin, auth
from mongodb_flask import database

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    # Set up a test database
    database.initialize_database(app)

    # Initialize Flask-Bcrypt
    bcrypt = Bcrypt(app)
    app.bcrypt = bcrypt

    # Create the API and add the namespace
    api = Api(app)
    api.add_namespace(auth)

    # Add routes to the app
    app.add_url_rule('/auth/register', view_func=UserRegistration.as_view('register'))
    app.add_url_rule('/auth/login', view_func=UserLogin.as_view('login'))

    yield app


# def test_user_registration(app):
#     with app.test_client() as client:
#         # Send a POST request to register a new user
#         data = {
#             'username': 'test_user',
#             'password': 'test_password'
#         }
#         response = client.post('/auth/register', json=data)
#         assert response.status_code == 201
#         assert response.json['message'] == 'User registered successfully'

#         # Verify that the user is inserted into the database
#         user = app.config['DATABASE'].users.find_one({'username': 'test_user'})
#         assert user is not None

def test_user_registration_duplicate_username(app):
    # Insert a user with the same username into the database
    app.config['DATABASE'].users.insert_one({
        'username': 'test_user',
        'password': app.bcrypt.generate_password_hash('test_password').decode('utf-8')
    })

    with app.test_client() as client:
        # Send a POST request to register a new user with the same username
        data = {
            'username': 'test_user',
            'password': 'test_password2'
        }
        response = client.post('/auth/register', json=data)
        assert response.status_code == 400
        assert response.json['message'] == 'User already exists.'

def test_user_login(app):
    # Insert a user into the database
    hashed_password = app.bcrypt.generate_password_hash('test_password').decode('utf-8')
    app.config['DATABASE'].users.insert_one({
        'username': 'test_user',
        'password': hashed_password
    })

    with app.test_client() as client:
        # Send a POST request to login with the correct credentials
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = client.post('/auth/login', json=data)
        assert response.status_code == 200
        assert response.json['message'] == 'User authenticated successfully'

def test_user_login_invalid_credentials(app):
    # Insert a user into the database
    hashed_password = app.bcrypt.generate_password_hash('test_password').decode('utf-8')
    app.config['DATABASE'].users.insert_one({
        'username': 'test_user',
        'password': hashed_password
    })

    with app.test_client() as client:
        # Send a POST request to login with incorrect credentials
        data = {
            'username': 'test_user',
            'password': 'wrong_password'
        }
        response = client.post('/auth/login', json=data)
        assert response.status_code == 400
        assert response.json['message'] == 'Invalid credentials.'
