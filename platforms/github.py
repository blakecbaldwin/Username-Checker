import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REQUEST_TIMEOUT = (2, 4)

def validate(username):
    # GitHub usernames: max 39 chars, no underscores, no double hyphens, no ending in hyphen
    return re.fullmatch(r"[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38}", username) is not None

def check(username):
    if not validate(username):
        return {"status": "Invalid", "url": None}

    try:
        url = f"https://api.github.com/users/{username}"
        headers = {"User-Agent": "username-checker"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

        if r.status_code == 200:
            return {"status": "Taken", "url": f"https://github.com/{username}"}
        elif r.status_code == 404:
            return {"status": "Available", "url": None}
        elif r.status_code in (403, 429):
            return {"status": f"Unknown ({r.status_code})", "url": None}
        else:
            return {"status": f"Error: {r.status_code}", "url": None}
    except Exception as e:
        return {"status": "Request Failed", "url": None}

github_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "Only a-z, 0-9, hyphens. Max 39 characters. No underscores or spaces."
}
