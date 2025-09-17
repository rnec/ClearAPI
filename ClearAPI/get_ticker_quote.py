# get_ticker_quote
import requests
from typing import List
from auth import get_auth_token
from config import API_BASE_URL, SUBSCRIPTION_KEY, USER_AGENT

def get_ticker_quote(ticker) -> dict:
    url = f"{API_BASE_URL}/v1/marketdata/quote?Ticker={ticker}"
    headers = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        "Authorization": f"Bearer {get_auth_token()}",
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        error_message = response.text
        raise requests.HTTPError(f"Erro na solicitação: {response.status_code} - {error_message}")