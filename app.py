from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

app = Flask(__name__)

def get_twitch_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    try:
        r = requests.post(url, params=params)
        r.raise_for_status()
        return r.json()["access_token"]
    except:
        return None

def check_username(username):
    results = {}

    # GitHub
    github_url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "username-checker"
    }
    try:
        r = requests.get(github_url, headers=headers)
        if r.status_code == 404:
            results["GitHub"] = {"status": "✅ Available", "url": None}
        elif r.status_code == 200:
            results["GitHub"] = {"status": "❌ Taken", "url": f"https://github.com/{username}"}
        else:
            results["GitHub"] = {"status": f"⚠️ Error ({r.status_code})", "url": None}
    except:
        results["GitHub"] = {"status": "⚠️ Request Failed", "url": None}

    # Steam
    steam_url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {
        "key": STEAM_API_KEY,
        "vanityurl": username
    }
    try:
        r = requests.get(steam_url, params=params)
        data = r.json()
        if data["response"]["success"] == 1:
            results["Steam"] = {"status": "❌ Taken", "url": f"https://steamcommunity.com/id/{username}"}
        else:
            results["Steam"] = {"status": "✅ Available", "url": None}
    except:
        results["Steam"] = {"status": "⚠️ Request Failed", "url": None}

    # Twitch
    twitch_token = get_twitch_access_token()
    if not twitch_token:
        results["Twitch"] = {"status": "⚠️ Auth Failed", "url": None}
    else:
        twitch_url = "https://api.twitch.tv/helix/users"
        headers = {
            "Client-ID": TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {twitch_token}"
        }
        try:
            r = requests.get(twitch_url, headers=headers, params={"login": username})
            if r.status_code != 200:
                results["Twitch"] = {"status": f"⚠️ Error ({r.status_code})", "url": None}
            elif r.json()["data"]:
                results["Twitch"] = {"status": "❌ Taken", "url": f"https://www.twitch.tv/{username}"}
            else:
                results["Twitch"] = {"status": "✅ Available", "url": None}
        except:
            results["Twitch"] = {"status": "⚠️ Request Failed", "url": None}

    # Roblox (POST request)
    roblox_url = "https://users.roblox.com/v1/usernames/users"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    payload = {
        "usernames": [username],
        "excludeBannedUsers": False
    }
    try:
        r = requests.post(roblox_url, headers=headers, json=payload)
        data = r.json()
        if data.get("data"):
            results["Roblox"] = {"status": "❌ Taken", "url": f"https://www.roblox.com/users/profile?username={username}"}
        else:
            results["Roblox"] = {"status": "✅ Available", "url": None}
    except:
        results["Roblox"] = {"status": "⚠️ Request Failed", "url": None}

    return results

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    username = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        if username:
            results = check_username(username)
    return render_template("index.html", username=username, results=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
