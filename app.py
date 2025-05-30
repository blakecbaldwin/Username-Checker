
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
    print(f"\n🔍 Checking username: {username}\n")

    # GitHub
    try:
        github_url = f"https://api.github.com/users/{username}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "username-checker"}
        r = requests.get(github_url, headers=headers)
        results["GitHub"] = {"status": "❌ Taken", "url": f"https://github.com/{username}"} if r.status_code == 200 else {"status": "✅ Available", "url": None}
    except:
        results["GitHub"] = {"status": "⚠️ Request Failed", "url": None}

    # Steam
    try:
        url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
        params = {"key": STEAM_API_KEY, "vanityurl": username}
        r = requests.get(url, params=params)
        data = r.json()
        results["Steam"] = {"status": "❌ Taken", "url": f"https://steamcommunity.com/id/{username}"} if data["response"]["success"] == 1 else {"status": "✅ Available", "url": None}
    except:
        results["Steam"] = {"status": "⚠️ Request Failed", "url": None}

    # Roblox
    try:
        url = "https://users.roblox.com/v1/usernames/users"
        headers = {"Content-Type": "application/json"}
        payload = {"usernames": [username], "excludeBannedUsers": False}
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()
        results["Roblox"] = {"status": "❌ Taken", "url": f"https://www.roblox.com/users/profile?username={username}"} if data.get("data") else {"status": "✅ Available", "url": None}
    except:
        results["Roblox"] = {"status": "⚠️ Request Failed", "url": None}

    # Minecraft
    try:
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        r = requests.get(url)
        results["Minecraft"] = {"status": "❌ Taken", "url": f"https://namemc.com/profile/{username}"} if r.status_code == 200 else {"status": "✅ Available", "url": None}
    except:
        results["Minecraft"] = {"status": "⚠️ Request Failed", "url": None}

    # Twitch
    twitch_token = get_twitch_access_token()
    if not twitch_token:
        results["Twitch"] = {"status": "⚠️ Auth Failed", "url": None}
    else:
        try:
            url = "https://api.twitch.tv/helix/users"
            headers = {"Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {twitch_token}"}
            r = requests.get(url, headers=headers, params={"login": username})
            data = r.json()
            results["Twitch"] = {"status": "❌ Taken", "url": f"https://www.twitch.tv/{username}"} if data.get("data") else {"status": "✅ Available", "url": None}
        except:
            results["Twitch"] = {"status": "⚠️ Request Failed", "url": None}

# TikTok
    try:
        url = f"https://www.tiktok.com/@{username}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 404:
            results["TikTok"] = {"status": "✅ Available", "url": None}
        elif r.status_code == 200:
            results["TikTok"] = {"status": "❌ Taken", "url": url}
        else:
            results["TikTok"] = {"status": f"⚠️ Error ({r.status_code})", "url": None}
    except:
        results["TikTok"] = {"status": "⚠️ Request Failed", "url": None}

    # Instagram
    try:
        url = f"https://www.instagram.com/{username}/"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 404:
            results["Instagram"] = {"status": "✅ Available", "url": None}
        elif r.status_code == 200:
            results["Instagram"] = {"status": "❌ Taken", "url": url}
        else:
            results["Instagram"] = {"status": f"⚠️ Error ({r.status_code})", "url": None}
    except:
        results["Instagram"] = {"status": "⚠️ Request Failed", "url": None}

    # YouTube
    try:
        url = f"https://www.youtube.com/@{username}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        results["YouTube"] = {"status": "❌ Taken", "url": url} if r.status_code == 200 else {"status": "✅ Available", "url": None}
    except:
        results["YouTube"] = {"status": "⚠️ Request Failed", "url": None}

    # Facebook
    try:
        url = f"https://www.facebook.com/{username}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if r.status_code == 404 or "content isn't available" in r.text.lower():
            results["Facebook"] = {"status": "✅ Available", "url": None}
        elif username.lower() in r.text.lower():
            results["Facebook"] = {"status": "❌ Taken", "url": url}
        else:
            results["Facebook"] = {"status": "⚠️ Unclear", "url": None}
    except:
        results["Facebook"] = {"status": "⚠️ Request Failed", "url": None}

    # Snapchat
    try:
        url = f"https://www.snapchat.com/add/{username}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        results["Snapchat"] = {"status": "❌ Taken", "url": url} if r.status_code == 200 else {"status": "✅ Available", "url": None}
    except:
        results["Snapchat"] = {"status": "⚠️ Request Failed", "url": None}

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
    app.run(debug=True, host="0.0.0.0", port=port)
