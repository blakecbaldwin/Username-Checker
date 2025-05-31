import re
import requests

def validate(username):
    return re.fullmatch(r"[a-zA-Z_\.][a-zA-Z0-9_\.]{1,23}", username) is not None

def check(username):
    try:
        url = f"https://www.tiktok.com/@{username}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36"
        }

        r = requests.get(url, headers=headers, timeout=5)
        html = r.text.lower()

        if "userinfo" in html:
            return {"status": "Taken", "url": url}
        else:
            return {"status": "Available", "url": None}
    except Exception as e:
        return {"status": f"Request Failed: {e}", "url": None}

tiktok_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "2–24 characters. Letters, numbers, underscores, and periods only."
}
