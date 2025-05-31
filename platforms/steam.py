import requests
import os
from dotenv import load_dotenv

load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

def validate(username):
    return 2 <= len(username) <= 32

def check(username):
    try:
        url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
        params = {"key": STEAM_API_KEY, "vanityurl": username}
        r = requests.get(url, params=params)
        data = r.json()
        if data["response"]["success"] == 1:
            return {"status": "Taken", "url": f"https://steamcommunity.com/id/{username}"}
        else:
            return {"status": "Available", "url": None}
    except:
        return {"status": "Request Failed", "url": None}

steam_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "2–32 characters. Letters and numbers only."
}
