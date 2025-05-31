import re
import requests

def validate(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{3,16}", username) is not None

def check(username):
    try:
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        r = requests.get(url)
        if r.status_code == 200:
            return {"status": "Taken", "url": f"https://namemc.com/profile/{username}"}
        else:
            return {"status": "Available", "url": None}
    except:
        return {"status": "Request Failed", "url": None}

minecraft_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "3–16 characters. Letters, numbers, underscores only."
}
