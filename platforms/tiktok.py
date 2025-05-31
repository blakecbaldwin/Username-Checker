import re
import requests
import time
import random

def validate(username):
    return re.fullmatch(r"[a-zA-Z_\.][a-zA-Z0-9_\.]{1,23}", username) is not None

def check(username):
    try:
        url = f"https://www.tiktok.com/@{username}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 Chrome/91.0 Mobile Safari/537.36"
        }

        r = requests.head(url, headers=headers, timeout=(1, 2), allow_redirects=False)
        if r.status_code == 200:
            return {"status": "Taken", "url": url}
        elif r.status_code in [301, 302, 404]:
            return {"status": "Available", "url": None}
        else:
            return {"status": f"Unknown: {r.status_code}", "url": None}
    except Exception as e:
        return {"status": f"Request Failed: {e}", "url": None}

tiktok_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "2–24 characters. Letters, numbers, underscores, and periods only."
}
