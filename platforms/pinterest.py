import re
import requests
from bs4 import BeautifulSoup

REQUEST_TIMEOUT = (2, 4)

def validate(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{3,30}", username) is not None

def check(username):
    try:
        url = f"https://www.pinterest.com/{username}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if r.status_code in (403, 429):
            return {"status": f"Unknown ({r.status_code})", "url": None}

        soup = BeautifulSoup(r.text, "html.parser")
        username_tag = soup.find("span", attrs={"data-test-id": "profile-username"})

        if username_tag and username_tag.text.strip().lower() == username.lower():
            return {"status": "Taken", "url": url}
        else:
            return {"status": "Available", "url": None}
    except Exception:
        return {"status": "Request Failed", "url": None}

pinterest_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "3–30 characters. Letters, numbers, and underscores only."
}
