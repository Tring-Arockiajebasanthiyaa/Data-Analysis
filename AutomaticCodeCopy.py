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
from configparser import Error
import dropbox.exceptions
import samplecode
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError,AuthError

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

def create_folder_if_not_exists(folder_path):
    try:
        dbx.files_get_metadata(folder_path)
        print("Folder already present")
    except ApiError as e:
        if isinstance(e.error, dropbox.files.GetMetadataError) and e.error.is_path() and e.error.get_path().is_not_found():
            dbx.files_create_folder_v2(folder_path)
            print("Folder created")
def upload_file_in_folder(file_path,dropbox_folder_path):
    dropbox_files_path = f"{dropbox_folder_path}/{os.path.basename(file_path)}"
    print("folder path:", dropbox_files_path)
    try:
        with open(file_path , "rb") as f:
            dbx.files_upload(f.read(),dropbox_files_path,mode=WriteMode('overwrite'))
            print("File uploaded")
    except ApiError as err:
            if (err.error.get_path() and err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
        
def search_dropbox(filename):
    try:
        results = dbx.files_search('', filename)
        list=[]
        if results.matches:
            print("Search results:")
            for match in results.matches:
                if isinstance(match, dropbox.files.SearchMatch):
                    print(f"- {match.metadata.path_display}")
                    list.append(match.metadata.path_display)
            return list           
        else:
            print(f"No files found matching '{filename}'.")
            return null

    except dropbox.exceptions.ApiError as err:
        print(f"Dropbox API error: {err}") 
        
def download_files(dropbox_path):
    try:
        current_dir = os.getcwd()
        relative_path = dropbox_path.lstrip("/")
        local_file_path = os.path.join(current_dir, relative_path)

        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        with open(local_file_path,'wb') as f:
            metadata,res=dbx.files_download(path=dropbox_path)
            f.write(res.content)
            print("Files downloaded")
    except ApiError as e:
        print(f"Error :{e}")
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
    folder_path=input("Enter the folder name to add your file(if the folder is missing then it create one):")
    if not folder_path.startswith('/'):
        folder_path = '/' + folder_path
    create_folder_if_not_exists(folder_path)
    local_path=input("Enter your entire file path:")
    if os.path.isfile(local_path):
        print("File present in it")
    else:
        print("File not present")
        sys.exit(1)
    upload_file_in_folder(local_path,folder_path)
    filename=input("Enter file name to search:")
    results=search_dropbox(filename)
    print(results)
    download_files(results[0])
    print("Done")
