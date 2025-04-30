import base64
import requests
import json

APP_KEY = 'fwoh8e8aey34oto'
APP_SECRET = 'ggiqq9eh4n1tenp'
ACCESS_CODE_GENERATED = 'EHOPR9Tdd_cAAAAAAAAAGQBd2lD_Pp9-tlNQV0O7PAI'

BASIC_AUTH = base64.b64encode(f'{APP_KEY}:{APP_SECRET}'.encode())

headers = {
    'Authorization': f"Basic {BASIC_AUTH}",
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = f'code={ACCESS_CODE_GENERATED}&grant_type=authorization_code'

response = requests.post('https://api.dropboxapi.com/oauth2/token',
                        data=data,
                        auth=(APP_KEY, APP_SECRET))
print(json.dumps(json.loads(response.text), indent=2))
