from flask import request, jsonify

from . import auth_bp
from .services import register_user, authenticate_user
from app import db

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        username = data.get('username').strip()
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        response, status = register_user(username, password)
        return jsonify(response), status

    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        username = data.get('username').strip()
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        response, status = authenticate_user(username, password)
        return jsonify(response), status

    except Exception:
        return jsonify({'error': 'Internal server error'}), 500
