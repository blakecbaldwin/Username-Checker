import re
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

# Cache token with expiration
_cached_token = None
_token_expiry = 0

def validate(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{4,25}", username) is not None

def get_token():
    global _cached_token, _token_expiry
    if _cached_token and time.time() < _token_expiry:
        return _cached_token

    try:
        r = requests.post("https://id.twitch.tv/oauth2/token", params={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        })
        data = r.json()
        _cached_token = data.get("access_token")
        expires_in = data.get("expires_in", 3600)  # default 1 hour
        _token_expiry = time.time() + expires_in - 60  # buffer before expiration
        return _cached_token
    except:
        return None

def check(username):
    token = get_token()
    if not token:
        return {"status": "Auth Failed", "url": None}
    try:
        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {token}"
        }
        r = requests.get("https://api.twitch.tv/helix/users", headers=headers, params={"login": username})
        if r.json().get("data"):
            return {"status": "Taken", "url": f"https://www.twitch.tv/{username}"}
        else:
            return {"status": "Available", "url": None}
    except:
        return {"status": "Request Failed", "url": None}

twitch_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "4–25 letters, numbers, and underscores only."
}
