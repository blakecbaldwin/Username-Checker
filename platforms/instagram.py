import re
import requests
import time
import random

REQUEST_TIMEOUT = (2, 4)

def validate(username):
    # Instagram usernames: 1–30 characters, letters, numbers, underscores, and periods
    return re.fullmatch(r"[a-zA-Z0-9_\.]{1,30}", username) is not None

def check(username):
    try:
        # Use realistic headers to avoid bot detection
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        url = f"https://www.instagram.com/{username}/"
        time.sleep(random.uniform(1.5, 2.5))  # avoid hitting rate limits

        r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

        if r.status_code == 404:
            return {"status": "Available", "url": None}
        elif r.status_code in (403, 429):
            return {"status": f"Unknown ({r.status_code})", "url": None}
        elif r.status_code == 200:
            html = r.text.lower()
            if "login" in html and "instagram" in html:
                return {"status": "Error", "url": None}  # maybe blocked or redirected
            else:
                return {"status": "Taken", "url": url}
        else:
            return {"status": f"Error ({r.status_code})", "url": None}
    except Exception as e:
        return {"status": f"Error: {e}", "url": None}

instagram_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "Up to 30 characters. Letters, numbers, underscores, and periods only."
}
