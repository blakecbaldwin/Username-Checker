import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def validate(username):
    # GitHub usernames: max 39 chars, no underscores, no double hyphens, no ending in hyphen
    return re.fullmatch(r"[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38}", username) is not None

def check(username):
    if not validate(username):
        print(f"[GitHub] Invalid username format: {username}")
        return {"status": "Invalid", "url": None}

    try:
        url = f"https://api.github.com/users/{username}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "User-Agent": "username-checker"
        }
        r = requests.get(url, headers=headers)
        print(f"[GitHub] Response code for {username}: {r.status_code}")

        if r.status_code == 200:
            return {"status": "Taken", "url": f"https://github.com/{username}"}
        elif r.status_code == 404:
            return {"status": "Available", "url": None}
        else:
            return {"status": f"Error: {r.status_code}", "url": None}
    except Exception as e:
        print(f"[GitHub] Exception: {e}")
        return {"status": "Request Failed", "url": None}

github_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "Only a-z, 0-9, hyphens. Max 39 characters. No underscores or spaces."
}
