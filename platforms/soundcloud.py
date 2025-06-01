import re
import requests

def validate(username):
    return re.fullmatch(r"[a-zA-Z0-9_-]{3,25}", username) is not None

def check(username):
    try:
        url = f"https://soundcloud.com/{username}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if r.status_code == 200:
            return {"status": "Taken", "url": url}
        elif r.status_code == 404:
            return {"status": "Available", "url": None}
        else:
            return {"status": "Unknown", "url": None}
    except:
        return {"status": "Request Failed", "url": None}

soundcloud_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "3–25 characters. Letters, numbers, hyphens, and underscores only."
}
