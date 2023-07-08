This is a simple flask-mongo db app that can be used a base for future applications.

---

# Flask-MongoDB Authentication App

This is a sample Flask-MongoDB authentication application that provides user registration and login functionality using Flask-RESTx, MongoDB, and Flask-Bcrypt.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration with validation for username and password
- Secure password storage using bcrypt
- User login with validation for username and password
- MongoDB database for storing user information
- Error handling and response formatting
- Logging for tracking application behavior


## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/flask-mongodb-auth-app.git
   ```

2. Change into the project directory:

   ```shell
   cd flask-mongodb-auth-app
   ```

3. Install Poetry:

   - Visit the [Poetry installation guide](https://python-poetry.org/docs/#installation) for instructions on how to install Poetry.

4. Install the project dependencies using Poetry:

   ```shell
   poetry install
   ```

5. Set up the MongoDB database:
   - Install MongoDB and start the MongoDB server.
   - Create a MongoDB database for the application.
   - Update the MongoDB connection details in the URI. 

6. Start the application:

   ```shell
   poetry shell
   python app.py
   ```

7. The application should now be running on `http://localhost:5000`.

---

By using Poetry, you can manage the project's dependencies, virtual environment, and packaging all in one tool. Ensure that you have Poetry installed, and follow the updated installation instructions provided above.

Feel free to modify and customize this section based on your specific project requirements.
## Usage

- Register a new user:
  - Endpoint: `/auth/register`
  - Method: `POST`
  - Request Body:
    ```json
    {
      "username": "your-username",
      "password": "your-password"
    }
    ```
  - Response: `{ "message": "User registered successfully" }`

- Login with an existing user:
  - Endpoint: `/auth/login`
  - Method: `POST`
  - Request Body:
    ```json
    {
      "username": "your-username",
      "password": "your-password"
    }
    ```
  - Response: `{ "message": "User authenticated successfully" }`

## API Endpoints

| Endpoint          | Method | Description                   |
| ----------------- | ------ | ----------------------------- |
| `/auth/register`  | POST   | Register a new user           |
| `/auth/login`     | POST   | Authenticate a user           |

## Technologies Used

- Flask: Python web framework
- Flask-RESTx: Extension for building REST APIs with Flask
- MongoDB: NoSQL database
- Flask-Bcrypt: Password hashing library
- Werkzeug: Web server gateway interface (WSGI) utility library

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

