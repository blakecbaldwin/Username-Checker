import re
import requests

REQUEST_TIMEOUT = (2, 4)

def validate(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{3,15}", username) is not None

def check(username):
    try:
        url = f"https://www.snapchat.com/add/{username}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return {"status": "Taken", "url": url}
        elif r.status_code in (403, 429):
            return {"status": f"Unknown ({r.status_code})", "url": None}
        else:
            return {"status": "Available", "url": None}
    except:
        return {"status": "Request Failed", "url": None}

snapchat_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "3–15 characters. Letters, numbers, and underscores only."
}
