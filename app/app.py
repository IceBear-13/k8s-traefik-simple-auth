from flask import Flask, request
import jwt
import os


app = Flask(__name__)

PORT = os.getenv('PORT', '5001')

@app.route('/')
def root():
    return {'message': 'Welcome to the API'}, 200

@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

@app.route('/hello')
def hello():
    token = request.headers.get('X-Token')
    if not token:
        return {'error': 'X-Token header is missing'}, 401

    try:
        print(token)
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        name = payload.get('name')
        if not name:
            return {'error': 'Name not found in token'}, 401
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}, 401
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}, 401
    
    return {'message': f'Hello, {name}!'}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)