from flask_jwt_extended import create_access_token

from app.models.user import User
from app import db
from .validators import validate_username, validate_password
from .utils import hash_password, verify_password

def register_user(username, password):
    is_valid, msg = validate_username(username)
    if not is_valid:
        return {"error": msg}, 400

    is_valid, msg = validate_password(password)
    if not is_valid:
        return {"error": msg}, 400

    # Check existing user
    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 409

    # Create user
    new_user = User(username=username, password_hash=hash_password(password))
    db.session.add(new_user)
    db.session.commit()

    return {
        "message": "User created successfully",
        "user_id": new_user.id,
        "username": new_user.username
    }, 201

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not verify_password(user.password_hash, password):
        return {"error": "Invalid username or password"}, 401

    token = create_access_token(identity=user.id)
    return {
        "message": "Login successful",
        "access_token": token,
        "user_id": user.id,
        "username": user.username
    }, 200
