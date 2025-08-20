from flask import Flask, request, Response
import jwt
import os

app = Flask(__name__)

PORT = os.getenv('PORT', '5000')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

@app.route('/auth')
def auth():
    print(f"JWT_SECRET_KEY: {JWT_SECRET_KEY}")  # Debug logging
    name = request.headers.get('name')
    print(f"Received name header: {name}")  # Debug logging
    
    if not name:
        return {'error': 'Name is required'}, 400

    if not JWT_SECRET_KEY:
        print("JWT_SECRET_KEY is None or empty")
        return {'error': 'JWT_SECRET_KEY not configured'}, 500

    payload = {
        'name': name
    }

    try:
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
        response = Response(status=200)
        response.headers['X-Token'] = token
        print(f"Generated token: {token}") 
        return response
    except Exception as e:
        print(f"JWT encoding error: {str(e)}") 
        return {'error': str(e)}, 500
    
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)