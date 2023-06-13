from flask import Flask, Blueprint, request, url_for, jsonify
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta


auth = Blueprint('auth', __name__)

# app = Flask(__name__)

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017')
db = client.eyecare  # database:eyecare

# User collection in the MongoDB database
users_collection = db.users


# Login endpoint
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Check if the user exists in the database
    user = users_collection.find_one({'email': email})

    if user and user['password'] == password:
        token = jwt.encode({'user': email, 'exp': datetime.utcnow() + timedelta(minutes=180)}, 'sample')
        return jsonify({'success': True, 'message': 'Login successful', 'token': token}), 200
    else:
        # Return error response
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401


@auth.route('/logout', methods=['POST'])
def logout():

    return jsonify({'success': True, 'message': 'Logout successful'}), 200

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    age = data['age']

    # Check if the username already exists
    if users_collection.find_one({'email': email}):
        return jsonify({'success': False, 'message': 'Username already exists'}), 400

    # Create the new user
    new_user = {
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'age': age
    }
    # Insert the new user into the database
    result = users_collection.insert_one(new_user)

    # Add the generated user ID to the user object
    new_user['id'] = str(result.inserted_id)

    # Return success response with the new user information
    return jsonify({'success': True, 'message': 'Signup successful', 'userid': str(result.inserted_id)}), 201


@auth.route('/profile/update', methods=['POST'])
def update_profile(logged_in_user_email):
    data = request.get_json()
    new_profile_data = data['profile_data']

    # Get the logged-in user's email from the authentication token or session
    # Assuming you have implemented the authentication mechanism

    # Find the user in the database based on the email
    user = users_collection.find_one({'email': logged_in_user_email})

    if user:
        # Update the user's profile data
        user['full_name'] = new_profile_data.get('full_name', user['full_name'])
        user['email'] = new_profile_data.get('email', user['email'])
        user['age'] = new_profile_data.get('age', user['age'])
        user['gender'] = new_profile_data.get('gender', user['gender'])
        user['password'] = new_profile_data.get('password', user['password'])

        # Save the updated user profile to the database

        # Return success response
        return jsonify({'success': True, 'message': 'Profile updated successfully'}), 200
    else:
        # Return error response
        return jsonify({'success': False, 'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run()
