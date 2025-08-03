from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get config from environment
API_URL = os.getenv('API_URL')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Build headers from environment
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://shahab.tbtb.ir',
    'referer': 'https://shahab.tbtb.ir/public/map/index',
    'requestverificationtoken': os.getenv('VERIFICATION_TOKEN'),
    'user-agent': os.getenv('USER_AGENT'),
    'x-requested-with': 'XMLHttpRequest'
}

# Build cookies from environment
COOKIES = {
    'arcaptcha': os.getenv('ARCAPTCHA_COOKIE'),
    'SessionCookie': os.getenv('SESSION_COOKIE'),
    'PrawAntiForgery': os.getenv('ANTIFORGERY_COOKIE')
}

@app.route('/outages')
def get_outages():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({'error': 'Need lat and lon parameters'}), 400
    
    try:
        float(lat)
        float(lon)
    except ValueError:
        return jsonify({'error': 'lat and lon must be numbers'}), 400
    
    data = f'Latitude={lat}&Longitude={lon}'
    
    try:
        logger.info(f"Making API request for lat={lat}, lon={lon}")
        
        response = requests.post(
            API_URL,
            headers=HEADERS,
            cookies=COOKIES,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info("API request successful")
            return response.json()
        else:
            logger.error(f"API request failed: {response.status_code}")
            return jsonify({
                'error': 'API request failed',
                'status_code': response.status_code,
                'message': response.text
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
        return jsonify({'error': 'Network error', 'message': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'outage-api'})

@app.route('/')
def home():
    return jsonify({
        'message': 'Power Outage API',
        'usage': '/outages?lat=<latitude>&lon=<longitude>',
        'example': '/outages?lat=35.75878319596661&lon=51.36180495377631'
    })

if __name__ == '__main__':
    logger.info(f"Starting server on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)