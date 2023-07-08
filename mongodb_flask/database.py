from pymongo import MongoClient

# Set the value of MONGODB_URI to your Atlas connection string.
MONGODB_URI = 'mongodb+srv://skanda:u9kOzbS3Exj47sdO@cluster0.fyxz25q.mongodb.net/'


def initialize_database(app):
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://skanda:u9kOzbS3Exj47sdO@cluster0.fyxz25q.mongodb.net/')
    db = client['user_db']
    app.config['DATABASE'] = db
