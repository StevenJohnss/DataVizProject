from datetime import timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from ..extension import db
from ..models.core import User  # Import the User model
from werkzeug.security import generate_password_hash, check_password_hash  # Import hashing functions
from .serliazers.serliazers import UserSchema
from marshmallow import ValidationError

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()  # Initialize JWT manager


# Route for user registration
@auth_bp.route('/register', methods=['POST'])
def register():
    # Define the UserSchema as shown above
    print("register route called")
    user_schema = UserSchema()
    try:
        # Validate and deserialize input
        user_data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400  # Return validation errors

    email = request.json.get('email')  # Get username from request
    password = request.json.get('password')  # Get password from request
    # Add user to the database
    new_user = User(email=email, password=generate_password_hash(password))  # Hash the password
    db.session.add(new_user)  # Add the new user to the session
    db.session.commit()  # Commit the session to save the user
    return jsonify({"msg": "User registered successfully"}), 201  # Return success message

# Route for user login
@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')  # Get username from request
    password = request.json.get('password')  # Get password from request
    user = User.query.filter_by(email=email).first()  # Query user by username
    if user and check_password_hash(user.password, password):  # Check hashed password
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=8))  # Create JWT token
        return jsonify(access_token=access_token), 200  # Return token
    return jsonify({"msg": "Bad username or password"}), 401  # Return error message

# Route for a protected resource
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()  # Require a valid JWT to access this route
def protected():
    return jsonify(msg="This is a protected route"), 200  # Return success message
