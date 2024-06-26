import os
import json
import requests
from dataclasses import dataclass
# from dotenv import load_dotenv

# load_dotenv()

@dataclass
class Settings:
    CLIENT_ID: str = os.environ.get("CLIENT_ID", "1721eff4-3ca4-4680-bec6-b5ce64056287")
    CLIENT_SECRET: str = os.environ.get("CLIENT_SECRET")
    TENANT: str = os.environ.get("TENANT")
    SCOPES: str = os.environ.get("SCOPES", 'api://1721eff4-3ca4-4680-bec6-b5ce64056287/User.Read openid profile email')
    FRONTEND: str = os.environ.get("FRONTEND", "http://localhost:8081")
    REDIRECT_URI: str = "http://localhost:8000/token"
    AUTHORITY_URL: str = "https://login.microsoftonline.com/common"  # f'https://login.microsoftonline.com/{self.TENANT}'
    AUTH_ENDPOINT: str = "/oauth2/v2.0/authorize"
    TOKEN_ENDPOINT: str = "/oauth2/v2.0/token"
    RESOURCE: str = "https://graph.microsoft.com/"
    API_VERSION: str = "beta"
    keys_url: str = "https://login.microsoftonline.com/common/discovery/keys"  # f'https://login.microsoftonline.com/{self.TENANT}/discovery/keys'
    keys_raw: str = requests.get(keys_url).text
    keys = json.loads(keys_raw)
