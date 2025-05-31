import re
import requests

def validate(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{3,20}", username) is not None

def check(username):
    try:
        url = "https://users.roblox.com/v1/usernames/users"
        headers = {"Content-Type": "application/json"}
        payload = {"usernames": [username], "excludeBannedUsers": False}
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()
        if data.get("data"):
            return {"status": "Taken", "url": f"https://www.roblox.com/users/profile?username={username}"}
        else:
            return {"status": "Available", "url": None}
    except:
        return {"status": "Request Failed", "url": None}

roblox_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "3–20 characters. No special characters allowed."
}
