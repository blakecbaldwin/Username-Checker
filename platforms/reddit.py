import re
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Cache token globally
access_token = None
token_expiry = 0

def get_reddit_token():
    global access_token, token_expiry

    if access_token and time.time() < token_expiry:
        return access_token

    auth = (os.getenv("REDDIT_CLIENT_ID"), os.getenv("REDDIT_CLIENT_SECRET"))
    headers = {"User-Agent": "username-checker/1.0"}
    data = {"grant_type": "client_credentials"}

    try:
        r = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers, timeout=5)
        r.raise_for_status()
        token_json = r.json()
        access_token = token_json["access_token"]
        token_expiry = time.time() + token_json["expires_in"] - 10  # renew 10s early
        return access_token
    except Exception as e:
        print(f"[Reddit] Failed to get token: {e}", flush=True)
        return None

def validate(username):
    return re.fullmatch(r"[A-Za-z0-9_-]{3,20}", username) is not None

def check(username):
    print(f"[Reddit] STARTING check for '{username}'", flush=True)

    token = get_reddit_token()
    if not token:
        return {"status": "Request Failed", "url": None}

    url = f"https://oauth.reddit.com/user/{username}/about"
    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": "username-checker/1.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"[Reddit] Status: {r.status_code} for '{username}'", flush=True)

        if r.status_code == 200:
            return {"status": "Taken", "url": f"https://www.reddit.com/user/{username}/"}
        elif r.status_code == 404:
            return {"status": "Available", "url": None}
        else:
            return {"status": f"Unknown ({r.status_code})", "url": None}
    except Exception as e:
        print(f"[Reddit] EXCEPTION: {e}", flush=True)
        return {"status": "Request Failed", "url": None}

reddit_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "3–20 characters. Letters, numbers, hyphens, and underscores only."
}
