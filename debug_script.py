#!/usr/bin/env python3
"""
Debug script to test the API directly and see what's happening
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get config from environment
API_URL = os.getenv('API_URL', 'https://shahab.tbtb.ir/public/map/v2/GetOutagesListByLatAndLong')

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

COOKIES = {
    'arcaptcha': os.getenv('ARCAPTCHA_COOKIE'),
    'SessionCookie': os.getenv('SESSION_COOKIE'),
    'PrawAntiForgery': os.getenv('ANTIFORGERY_COOKIE')
}

def debug_api_call():
    print("=== API Debug Test ===")
    print(f"API URL: {API_URL}")
    print(f"Headers: {HEADERS}")
    print(f"Cookies: {COOKIES}")
    print()
    
    # Test coordinates
    lat = "35.75878319596661"
    lon = "51.36180495377631"
    data = f'Latitude={lat}&Longitude={lon}'
    
    print(f"Testing with: lat={lat}, lon={lon}")
    print(f"Data payload: {data}")
    print()
    
    try:
        print("Making request...")
        response = requests.post(
            API_URL,
            headers=HEADERS,
            cookies=COOKIES,
            data=data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Content Length: {len(response.content)}")
        print(f"Content Type: {response.headers.get('content-type', 'Unknown')}")
        print()
        
        if response.text:
            print("Raw Response:")
            print("=" * 50)
            print(response.text)
            print("=" * 50)
        else:
            print("Empty response!")
        
        # Try to parse as JSON
        try:
            json_data = response.json()
            print("\nParsed JSON:")
            print(json_data)
        except Exception as e:
            print(f"\nJSON Parse Error: {e}")
        
    except Exception as e:
        print(f"Request failed: {e}")

def test_without_auth():
    print("\n=== Testing without authentication ===")
    
    lat = "35.75878319596661"
    lon = "51.36180495377631"
    data = f'Latitude={lat}&Longitude={lon}'
    
    simple_headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36'
    }
    
    try:
        response = requests.post(API_URL, headers=simple_headers, data=data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == '__main__':
    debug_api_call()
    test_without_auth()