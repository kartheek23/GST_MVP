import requests
import pandas as pd
from app.config import SANDBOX_BASE_URL, API_VERSION

class SandboxGSTClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = None
    
    def authenticate(self):
        url = f"{SANDBOX_BASE_URL}/authenticate"
        headers = {
            "x-api-key": self.api_key,
            "x-api-secret": self.api_secret,
            "x-api-version": API_VERSION
        }

        res = requests.post(url, headers=headers)
        res.raise_for_status()

        self.access_token = res.json()["data"]["access_token"]

    def fetch_b2b_invoices(self):
        url = f"{SANDBOX_BASE_URL}/gst/compliance/tax-payer/invoices?section=b2b"
        headers = {
            "Authorization": self.access_token,
            "x-api-key": self.api_key,
            "x-api-version": API_VERSION
        }
        res = requests.get(url, headers=headers)
        res.raise_for_status()

        data = res.json()['data']['data']['b2b']
        return pd.DataFrame(data)