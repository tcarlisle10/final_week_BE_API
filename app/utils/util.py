from flask import request, jsonify
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

# Create a token
def encode_token(mechanic_id):
    """
    Generates a JWT token with mechanic ID and expiration time.
    """
    try:
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=1),
            'iat': datetime.now(timezone.utc),
            'sub': mechanic_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return str(e)

def token_required(f):
    """
    Decorator to validate JWT tokens in Authorization header.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  
            except IndexError:
                return jsonify({'message': 'Token is missing'}), 401
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_mechanic = data['sub']  
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_mechanic, *args, **kwargs)
    return decorated

# admin_required wrapper
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split()[1]

                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print("PAYLOAD:", payload)
            except jwt.ExpiredSignatureError:
                return jsonify({'message': "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid Token"}), 401

            if payload['role'] == 'admin':
                return func(*args, **kwargs)  
            else:
                return jsonify({"messages": "Admin Authorization Required"}), 401
        else:
            return jsonify({"messages": "Token Authorization Required"}), 401

    return wrapper
