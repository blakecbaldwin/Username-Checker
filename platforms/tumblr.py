import re
import requests

def validate(username):
    # Allow upper/lowercase input but validate against lowercase rules
    return re.fullmatch(r"[a-zA-Z0-9-]{3,32}", username) is not None

def check(username):
    try:
        username = username.lower()  # Normalize to lowercase for Tumblr
        url = f"https://{username}.tumblr.com/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 404:
            return {"status": "Available", "url": None}
        elif response.status_code == 200:
            return {"status": "Taken", "url": url}
        else:
            return {"status": "Unknown", "url": None}
    except Exception as e:
        print(f"[Tumblr] Exception: {e}")
        return {"status": "Request Failed", "url": None}

tumblr_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "3–32 characters. Letters, numbers, and hyphens allowed. Case-insensitive."
}
