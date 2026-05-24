import re
import requests

REQUEST_TIMEOUT = (2, 4)

def validate(username):
    return re.fullmatch(r"[a-zA-Z_\.][a-zA-Z0-9_\.]{1,23}", username) is not None

def check(username):
    try:
        url = f"https://www.tiktok.com/@{username}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36"
        }

        r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        html = r.text.lower()

        if r.status_code in (403, 429):
            return {"status": f"Unknown ({r.status_code})", "url": None}
        elif "userinfo" in html:
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
