from flask import Flask
from flask_restx import Api
from auth import auth
from database import initialize_database
from flask_bcrypt import Bcrypt

app = Flask(__name__)

api = Api(
    app,
    title='A Simple Flask and MongoDB app',
    version='1.0',
    description='A description'
)

# Initialize the database
initialize_database(app)

# Register the API blueprint
api.add_namespace(auth)

if __name__ == '__main__':
    app.run(debug=True)
