from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

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
    github_headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "username-checker"
    }
    try:
        r = requests.get(github_url, headers=github_headers)
        if r.status_code == 404:
            results["GitHub"] = "✅ Available"
        elif r.status_code == 200:
            results["GitHub"] = "❌ Taken"
        else:
            results["GitHub"] = f"⚠️ Error ({r.status_code})"
    except:
        results["GitHub"] = "⚠️ Request Failed"

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
            results["Steam"] = "❌ Taken"
        else:
            results["Steam"] = "✅ Available"
    except:
        results["Steam"] = "⚠️ Request Failed"

    # Twitch
    twitch_token = get_twitch_access_token()
    if not twitch_token:
        results["Twitch"] = "⚠️ Auth Failed"
    else:
        twitch_url = f"https://api.twitch.tv/helix/users"
        headers = {
            "Client-ID": TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {twitch_token}"
        }
        try:
            r = requests.get(twitch_url, headers=headers, params={"login": username})
            if r.status_code != 200:
                results["Twitch"] = f"⚠️ Error ({r.status_code})"
            elif r.json()["data"]:
                results["Twitch"] = "❌ Taken"
            else:
                results["Twitch"] = "✅ Available"
        except:
            results["Twitch"] = "⚠️ Request Failed"
    
    # Roblox
    roblox_url = f"https://api.roblox.com/users/get-by-username?username={username}"
    try:
        r = requests.get(roblox_url)
        data = r.json()
        if "Id" in data and data["Id"] != 0:
            results["Roblox"] = "❌ Taken"
        else:
            results["Roblox"] = "✅ Available"
    except:
        results["Roblox"] = "⚠️ Request Failed"

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
