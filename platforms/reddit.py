import re
import requests

def validate(username):
    return re.fullmatch(r"[A-Za-z0-9_-]{3,20}", username) is not None

def check(username):
    try:
        url = f"https://www.reddit.com/user/{username}/about.json"
        headers = {"User-Agent": "UsernameChecker/1.0"}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            return {"status": "Taken", "url": f"https://www.reddit.com/user/{username}"}
        elif response.status_code == 404:
            return {"status": "Available", "url": None}
        else:
            return {"status": f"Error: {response.status_code}", "url": None}
    except Exception as e:
        return {"status": f"Request Failed: {e}", "url": None}

reddit_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "3–20 characters. Letters, numbers, underscores, and hyphens allowed."
}
