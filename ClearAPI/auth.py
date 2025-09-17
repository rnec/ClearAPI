# auth.py
import requests
from config import SUBSCRIPTION_KEY, API_KEY, API_SECRET, USER_AGENT

_auth_url = 'https://api-parceiros.xpi.com.br/variableincome-openapi-auth/v1/auth'

def get_auth_token() -> str:
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'User-Agent': USER_AGENT
    }
    payload = {
        'API_KEY': API_KEY,
        'API_SECRET': API_SECRET
    }

    response = requests.post(_auth_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        return token
    else:
        error_message = response.text
        raise requests.HTTPError(f"Erro na solicitação: {response.status_code} - {error_message}")