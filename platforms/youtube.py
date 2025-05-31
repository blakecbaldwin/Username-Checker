import re
import requests

def validate(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{1,30}", username) is not None

def check(username):
    try:
        url = f"https://www.youtube.com/@{username}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            return {"status": "Taken", "url": url}
        else:
            return {"status": "Available", "url": None}
    except:
        return {"status": "Request Failed", "url": None}

youtube_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "Letters, numbers, underscores only."
}