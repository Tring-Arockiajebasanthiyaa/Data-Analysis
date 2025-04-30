# import http.server
# import socketserver
# import webbrowser
# import requests
# import threading
# import json
# import urllib.parse
# import sys

# APP_KEY = 'fwoh8e8aey34oto'
# APP_SECRET = 'ggiqq9eh4n1tenp'
# REDIRECT_URI = 'http://localhost:8080'

# authorization_code = None

# class OAuthHandler(http.server.BaseHTTPRequestHandler):
#     def do_GET(self):
#         global authorization_code
#         parsed_path = urllib.parse.urlparse(self.path)
#         params = urllib.parse.parse_qs(parsed_path.query)
#         if 'code' in params:
#             authorization_code = params['code'][0]
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(b"<html><body><h2>Authorization successful. You can close this window.</h2></body></html>")
#         else:
#             self.send_response(400)
#             self.end_headers()
#             self.wfile.write(b"<html><body><h2>Error: Authorization code not found.</h2></body></html>")

# def start_local_server():
#     with socketserver.TCPServer(("", 8080), OAuthHandler) as httpd:
#         print("Starting local server at http://localhost:8080")
#         httpd.handle_request() 

# def open_authorization_url():
#     auth_url = (
#         f"https://www.dropbox.com/oauth2/authorize"
#         f"?client_id={APP_KEY}"
#         f"&response_type=code"
#         f"&token_access_type=offline"
#         f"&redirect_uri={REDIRECT_URI}"
#     )
#     print(f"Opening browser for authorization:\n{auth_url}")
#     webbrowser.open(auth_url)

# def get_tokens(auth_code):
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }

#     data = {
#         'code': auth_code,
#         'grant_type': 'authorization_code',
#         'client_id': APP_KEY,
#         'client_secret': APP_SECRET,
#         'redirect_uri': REDIRECT_URI
#     }

#     response = requests.post('https://api.dropboxapi.com/oauth2/token', headers=headers, data=data)

#     if response.status_code == 200:
#         tokens = response.json()
#         print("\n=== Tokens Successfully Generated ===")
#         print(json.dumps(tokens, indent=2))
#         return tokens
#     else:
#         print("\nError during token exchange:")
#         print(response.text)
#         sys.exit(1)


# if __name__ == '__main__':
#     server_thread = threading.Thread(target=start_local_server)
#     server_thread.start()

#     open_authorization_url()

#     while authorization_code is None:
#         pass

#     get_tokens(authorization_code)

import http.server
import socketserver
import webbrowser
import requests
import threading
import json
import urllib.parse
import sys
import os
import dropbox
APP_KEY = 'fwoh8e8aey34oto'
APP_SECRET = 'ggiqq9eh4n1tenp'
REDIRECT_URI = 'http://localhost:8080'
REFRESH_TOKEN_FILE = 'refresh_token.txt'

authorization_code = None


class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global authorization_code
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)
        if 'code' in params:
            authorization_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h2>Authorization successful. You can close this window.</h2></body></html>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<html><body><h2>Error: Authorization code not found.</h2></body></html>")


def start_local_server():
    with socketserver.TCPServer(("", 8080), OAuthHandler) as httpd:
        print("Starting local server at http://localhost:8080")
        httpd.handle_request()


def open_authorization_url():
    auth_url = (
        f"https://www.dropbox.com/oauth2/authorize"
        f"?client_id={APP_KEY}"
        f"&response_type=code"
        f"&token_access_type=offline"
        f"&redirect_uri={REDIRECT_URI}"
    )
    print(f"Opening browser for authorization:\n{auth_url}")
    webbrowser.open(auth_url)


def save_refresh_token(token):
    with open(REFRESH_TOKEN_FILE, 'w') as f:
        f.write(token)


def load_refresh_token():
    if os.path.exists(REFRESH_TOKEN_FILE):
        with open(REFRESH_TOKEN_FILE, 'r') as f:
            return f.read().strip()
    return None


def get_tokens(auth_code=None):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    if auth_code:
        data = {
            'code': auth_code,
            'grant_type': 'authorization_code',
            'client_id': APP_KEY,
            'client_secret': APP_SECRET,
            'redirect_uri': REDIRECT_URI
        }
        response = requests.post('https://api.dropboxapi.com/oauth2/token', headers=headers, data=data)
        if response.status_code == 200:
            tokens = response.json()
            print("\n=== Tokens Retrieved with Authorization Code ===")
            print(json.dumps(tokens, indent=2))
            if 'refresh_token' in tokens:
                save_refresh_token(tokens['refresh_token'])
            return tokens
        else:
            print("\nError getting tokens with authorization code:")
            print(response.text)
            sys.exit(1)
    else:
        refresh_token = load_refresh_token()
        if not refresh_token:
            print("No refresh token found. Please authorize first.")
            return None
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': APP_KEY,
            'client_secret': APP_SECRET
        }
        response = requests.post('https://api.dropboxapi.com/oauth2/token', headers=headers, data=data)
        if response.status_code == 200:
            tokens = response.json()
            print("\nAccess Token Retrieved from Refresh Token")
            print(json.dumps(tokens, indent=2))
            return tokens
        else:
            print("\nError refreshing token:")
            print(response.text)
            return None


if __name__ == '__main__':

    tokens = get_tokens()

    if not tokens:
        server_thread = threading.Thread(target=start_local_server)
        server_thread.start()
        open_authorization_url()

        while authorization_code is None:
            pass

        tokens = get_tokens(authorization_code)

    print("\nAccess Token:")
    print(tokens.get('access_token'))
    access_token=tokens.get('access_token')
    dbx=dropbox.Dropbox(access_token)
    print("Done")
