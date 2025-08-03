#!/usr/bin/env python3
"""
Helper script to update cookies in .env file
Run this when you get fresh cookies from browser
"""

def update_env_file():
    print("Paste your new cURL command here:")
    print("(Right-click on network request → Copy → Copy as cURL)")
    print()
    
    curl_command = input("cURL command: ").strip()
    
    if not curl_command.startswith('curl'):
        print("Error: Please paste a valid cURL command")
        return
    
    # Extract cookies from cURL command
    import re
    
    # Find the -b flag with cookies
    cookie_match = re.search(r"-b '([^']+)'", curl_command)
    if not cookie_match:
        cookie_match = re.search(r'-b "([^"]+)"', curl_command)
    
    if not cookie_match:
        print("Error: No cookies found in cURL command")
        return
    
    cookies_string = cookie_match.group(1)
    
    # Parse individual cookies
    cookies = {}
    for cookie in cookies_string.split('; '):
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookies[key] = value
    
    # Find verification token in headers
    token_match = re.search(r"'requestverificationtoken: ([^']+)'", curl_command)
    if not token_match:
        token_match = re.search(r'"requestverificationtoken: ([^"]+)"', curl_command)
    
    verification_token = token_match.group(1) if token_match else ""
    
    # Update .env file
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        with open('.env', 'w') as f:
            for line in lines:
                if line.startswith('ARCAPTCHA_COOKIE='):
                    f.write(f"ARCAPTCHA_COOKIE={cookies.get('arcaptcha', '')}\n")
                elif line.startswith('SESSION_COOKIE='):
                    f.write(f"SESSION_COOKIE={cookies.get('SessionCookie', '')}\n")
                elif line.startswith('ANTIFORGERY_COOKIE='):
                    f.write(f"ANTIFORGERY_COOKIE={cookies.get('PrawAntiForgery', '')}\n")
                elif line.startswith('VERIFICATION_TOKEN='):
                    f.write(f"VERIFICATION_TOKEN={verification_token}\n")
                else:
                    f.write(line)
        
        print("✅ Cookies updated successfully!")
        print("Restart your app to use the new cookies.")
        
    except Exception as e:
        print(f"Error updating .env file: {e}")

if __name__ == '__main__':
    update_env_file()