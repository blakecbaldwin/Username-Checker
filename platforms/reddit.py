import re
import requests

def validate(username):
    return re.fullmatch(r"[A-Za-z0-9_-]{3,20}", username) is not None

def check(username):
    try:
        url = f"https://www.reddit.com/user/{username}/about.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; username-checker/1.0)"
        }
        r = requests.get(url, headers=headers, timeout=5)

        if r.status_code == 200:
            return {"status": "Taken", "url": f"https://www.reddit.com/user/{username}/"}
        elif r.status_code == 404:
            return {"status": "Available", "url": None}
        else:
            return {"status": "Unknown", "url": None}
    except:
        return {"status": "Request Failed", "url": None}

reddit_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "3–20 characters. Letters, numbers, hyphens, and underscores only."
}
