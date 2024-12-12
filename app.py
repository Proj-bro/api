import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# Configure CORS with flexible settings
cors_config = {
    'origins': [
        'http://localhost:8000',  # Local development
        'https://localhost:8000',
        'https://*.onrender.com',  # All Render subdomains
        'http://*.onrender.com',
        # Add your specific frontend URLs here
    ]
}
CORS(app, resources={
    r"/*": {
        "origins": cors_config['origins'],
        "allow_headers": [
            "Content-Type", 
            "Authorization", 
            "Access-Control-Allow-Credentials"
        ],
        "supports_credentials": True
    }
})

@app.route('/api/v1/get-horoscope/daily', methods=['GET'])
def get_horoscope():
    try:
        # Get parameters from the request
        sign = request.args.get('sign')
        day = request.args.get('day')

        # Validate input
        if not sign or not day:
            return jsonify({
                'success': False, 
                'error': 'Missing sign or day parameter'
            }), 400

        # Make request to external API
        api_url = f"https://hor-769y.onrender.com/api/v1/get-horoscope/daily?sign={sign}&day={day}"
        
        # Fetch data from external API
        response = requests.get(api_url)
        
        # Check if request was successful
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'success': False, 
                'error': 'Failed to fetch horoscope data',
                'status_code': response.status_code
            }), 500

    except requests.RequestException as e:
        # Handle network-related errors
        return jsonify({
            'success': False, 
            'error': f'Network error: {str(e)}'
        }), 503
    except Exception as e:
        # Catch any other unexpected errors
        return jsonify({
            'success': False, 
            'error': f'Unexpected error: {str(e)}'
        }), 500

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message': 'API is running successfully'
    }), 200

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

if __name__ == '__main__':
    # Use PORT environment variable for Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)