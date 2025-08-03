from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Headers and cookies from the curl command
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,de-US;q=0.8,de;q=0.7,fa-US;q=0.6,fa;q=0.5,ja-US;q=0.4,ja;q=0.3,cs-CZ;q=0.2,cs;q=0.1',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://shahab.tbtb.ir',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://shahab.tbtb.ir/public/map/index',
    'requestverificationtoken': 'CfDJ8E8xybVDEI1CuE4vFTSKLBYfcYWMJjtMtuc5EQoZk-XM2rszznB6wTFUSKI5vS2HgFlWVqHs4nPS13H_JzqjM6uV0B2GWEEcuKo21LvC9Nf8pJ6oeVlYMVhuAN4kktVCcZ1M3Vt32_GNpn-l-aeQiFg',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

COOKIES = {
    'arcaptcha': '6a3acf69b3d87ee79849ee2aad40d6d9',
    'SessionCookie': 'CfDJ8E8xybVDEI1CuE4vFTSKLBZIwjvecbhiIo8fGgxiOj71%2FItEOhzdpqlQ8NaqPrvcLCnaMqsHLLg25rGeB%2BUHNutQ3dRE4BxuDeFAvU2sAS5UY2mGVMaELYaEkVTjK6epu7F%2B0e0GLFi4afaoplHKcsATp6vWAgMWiLy0dLGbFNBC',
    'PrawAntiForgery': 'CfDJ8E8xybVDEI1CuE4vFTSKLBaHcDxUfm7CF41NVThD6xZF91_PcFNSDWTTgbXaOJEb4u69G90WDy-ooBSPdF4pZ__m7PSD_YTzr2aG3GxPzaxp4yyO41oWD9ixzfX5WJcdf0BCuPtnl8fVdGr1C0b1mI8'
}

API_URL = 'https://shahab.tbtb.ir/public/map/v2/GetOutagesListByLatAndLong'

@app.route('/outages', methods=['GET'])
def get_outages():
    """
    Get power outages by latitude and longitude
    
    Query parameters:
    - lat: latitude (required)
    - lon: longitude (required)
    
    Example: /outages?lat=35.75878319596661&lon=51.36180495377631
    """
    try:
        # Get latitude and longitude from query parameters
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not lat or not lon:
            return jsonify({
                'error': 'Missing required parameters',
                'message': 'Both lat and lon parameters are required'
            }), 400
        
        # Validate lat/lon are numeric
        try:
            float(lat)
            float(lon)
        except ValueError:
            return jsonify({
                'error': 'Invalid parameters',
                'message': 'lat and lon must be valid numbers'
            }), 400
        
        # Prepare the data payload
        data = f'Latitude={lat}&Longitude={lon}'
        
        # Make the API request
        response = requests.post(
            API_URL,
            headers=HEADERS,
            cookies=COOKIES,
            data=data
        )
        
        # Return the raw response
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({
                'error': 'API request failed',
                'status_code': response.status_code,
                'message': response.text
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Network error',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Server error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with usage instructions"""
    return jsonify({
        'message': 'Power Outage API Server',
        'usage': 'GET /outages?lat=<latitude>&lon=<longitude>',
        'example': '/outages?lat=35.75878319596661&lon=51.36180495377631',
        'health': 'GET /health'
    })

if __name__ == '__main__':
    print("Starting Power Outage API Server...")
    print("Usage: GET /outages?lat=<latitude>&lon=<longitude>")
    print("Example: http://localhost:5000/outages?lat=35.75878319596661&lon=51.36180495377631")
    app.run(debug=True, host='0.0.0.0', port=5000)
