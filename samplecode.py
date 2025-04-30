from configparser import Error
import json
import sys

import dropbox.exceptions
import samplecode
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import webbrowser
import requests
import os
# TOKEN = "sl.u.AFtRuZ4Y6325POy73Qz69jI9FFNcFAigrU07IU2GB5HLMg9iQK2oYudYYFqYPnK4r-cGaYaBEAZ9eUbFK1vR-0Kk7ri_K0DGx7gexZ8z5gnybVL3TFmPUMBRIohvd8Okp3XSL44RLg0qlW__6YSF0hrG5-pSe7PfbEugcbBY5BDeWRRhgbAcooBXUXZHZmH781cQo-W3A98ZOQkRAum_lmcN3uKvj193IutaqKZ61_O5saRZcJ77jSpc2jejIN_nnxUfOx3kEX9v1MKl7UBsLrgjZLYM2O-ltUEVvpl8bHS2XyZIf5KeyZQsrO3R7CaR00DXj0h_1nf8vblYViDBVWADHqCI06MwXV-86ttscKQnGclMMPITCMJgOAa8YTZSpCnMQE7smT-ZsI66wABAKuj2ksNivhGk86QwNuJs43MYGl9wePeCCdJWK9JlzoeTFPQz1kKYwMVl4NcQ23A_EE_LUXxgLIzwQlvop4qdx-PjdxwPKRxLY8AWgvoW4PHPn3MjPbnjGjWrwqPzr4rzoNV94P_4VzItCLPLDyENFtPnABphv8aQVL0rU9xeI6kvgOSPijQGx8yAhvAWmQo5RNljmojMRv4QTxXOfyFhqOFMuFU-U8d-QGqTQeCR-q0uDlFhjSVrLmzUyIkx7zKAOzF9ZqTc0rgMzXXlIkjPMWTUivhYmx6TLBs953pigVqg0Pg9qb1KIB7QcRTsr5VN-Tve-BNmXalUJ8fRVQr6dL9lf6rsjOz9xKsxGTZrkkfWXUdum277iV3xRVBDfj12UtBZZQTx5Oj-aGPV6orbb9YTMsxyxhwu0QA9Q5efPducGjyZBFAvOgMUlttrU4TXT84hVLgM6QyZtuqOb4NhBUO3UrcZIr4OweJylQ372f8LHn8SNrC90eremyXuRGuKr7c09Idt_8jD4bLo3M1NHjQZt10Suy4LA8VKCzqzxO853Fjfdt0fDyAy3k9fftveafNtgDBxVtIb202q7DXQjys_-kEZDd9Lq5MUv4nAhDA5rh-5e-saQJwipZ7L4JL46BFWEqp3tyPQ15CHbP1EE18Lf0SrKecUz92DHFAcKDjiKtNyZ9hPuwH5JjV0Cbuc3Jg9YG_2E6mDAcRcDFQchTmazxTmxnA67tta9uIjkzpzxWst1AKU5pWBVPqIcm9DRXeQsKgkF7_ACkR5EzG795iEMrHEHP4OimpHtUVp1RVQN2xPhrqJa2uMNWKSS2P4x4LJVG5ZrDHvn7gubOyRd4nD7RZWs4rKsd2tKlzMcPcfM1NrG4iqJ8bnJc59sy07kgu0ycAC5DdADgPI8iXYWq5l_MUG04rnO8Oh0k7wPgdySF7NbkgwzM9Vj56PYlb_MtTo90lnoW2ZjYgfZp9Vyuq2LNBVqe23fd55wGgAFZQ5jJTScAGOefR7lMXEKH-RqGlZcAw_IKS0IKRoEbCybSBZHOXn5YNTTIUSnOWyvinZ_j4"

LOCALFILE = 'C:\PyTask\TextFiles\samplefile.txt'
BACKUPPATH = '/Sample/DestFile.txt' 


APP_KEY = 'fwoh8e8aey34oto'
APP_SECRET = 'ggiqq9eh4n1tenp'

def open_authorization_url():
    auth_url = f'https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&response_type=code&token_access_type=offline'
    print(f"Opening authorization URL:\n{auth_url}")
    webbrowser.open(auth_url)

def get_tokens(auth_code):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'code': auth_code,
        'grant_type': 'authorization_code',
        'client_id': APP_KEY,
        'client_secret': APP_SECRET,
    }

    response = requests.post('https://api.dropboxapi.com/oauth2/token', headers=headers, data=data)

    if response.status_code == 200:
        tokens = response.json()
        print("\n=== Tokens Successfully Generated ===")
        print(json.dumps(tokens, indent=2))
        return tokens
    else:
        print("\nError during token exchange:")
        print(response.text)
        sys.exit(1)
def backup():
    with open(LOCALFILE, 'rb') as f:
        
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


def checkFileDetails():
    print("Checking file details")

    for entry in dbx.files_list_folder('').entries:
        print("File list is : ")
        print(entry.name)

def downloadFile():
    sample_file = 'DestFile.txt'
    localPath = os.path.join(os.getcwd(), sample_file)

    result = dbx.files_list_folder('', recursive=True)
    entries = result.entries

    while result.has_more:
        result = dbx.files_list_folder_continue(result.cursor)
        entries.extend(result.entries)

    for entry in entries:
        if searchFileInDropbox(sample_file, entry):
            try:
                metadata, response = dbx.files_download(path=entry.path_display)
                with open(localPath, 'wb') as f:
                    f.write(response.content)
                print(f"File '{sample_file}' downloaded to the current directory!")
                return True
            except dropbox.exceptions.ApiError as err:
                print(f"Error downloading file: {err}")
                return False

    print(f"File '{sample_file}' not found in Dropbox.")
    return False

def searchFileInDropbox(filename, entry):
    if isinstance(entry, dropbox.files.FileMetadata) and entry.name == filename:
        return True
    return False

def createFolderIfNotExists(folderName):
    try:
        dbx.files_get_metadata(folderName)
        print("Folder present")
    except ApiError as e:
        if isinstance(e.error, dropbox.files.GetMetadataError) and e.error.is_path() and e.error.get_path().is_not_found():
            dbx.files_create_folder_v2(folderName)
    else:
        raise
if __name__ == '__main__':
    open_authorization_url()
    auth_code = input("\nAfter authorizing, paste the code you received here: ").strip()
    tokens = get_tokens(auth_code)
    
    access_token = tokens.get('access_token')
    if not access_token:
        sys.exit("ERROR: Access token not found!")

    print("\nCreating Dropbox object...")
    dbx = dropbox.Dropbox(access_token)
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    try:
        checkFileDetails()
    except Error as err:
        sys.exit("Error while checking file details")
    folderName=input("Enter the folder name:")
    if not folderName.startswith('/'):
        folderName = '/' + folderName
    createFolderIfNotExists(folderName)
    print("Creating backup...")
    backup()
    print("File Uploaded")
    downloadFile()
    print("Done!")
