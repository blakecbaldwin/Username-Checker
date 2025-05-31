from flask import Flask, render_template, request
import requests
import os
import time
import random
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

app = Flask(__name__)

# --- Username validation rules ---
def is_valid_github(username):
    return re.fullmatch(r"[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}", username, re.IGNORECASE) is not None

def is_valid_tiktok(username):
    return re.fullmatch(r"[a-zA-Z_\.][a-zA-Z0-9_\.]{1,23}", username) is not None

def is_valid_instagram(username):
    return re.fullmatch(r"[a-zA-Z0-9_\.]{1,30}", username) is not None

def is_valid_facebook(username):
    return re.fullmatch(r"[a-zA-Z0-9\.]{5,50}", username) is not None

def is_valid_youtube(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{1,30}", username) is not None

def is_valid_snapchat(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{3,15}", username) is not None

def is_valid_roblox(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{3,20}", username) is not None

def is_valid_twitch(username):
    return re.fullmatch(r"[a-z0-9_]{4,25}", username) is not None

def is_valid_minecraft(username):
    return re.fullmatch(r"[a-zA-Z0-9_]{3,16}", username) is not None

def is_valid_steam(username):
    return 2 <= len(username) <= 32  # Vanity URLs are loosely validated

validation_map = {
    "GitHub": is_valid_github,
    "TikTok": is_valid_tiktok,
    "Instagram": is_valid_instagram,
    "Facebook": is_valid_facebook,
    "YouTube": is_valid_youtube,
    "Snapchat": is_valid_snapchat,
    "Roblox": is_valid_roblox,
    "Twitch": is_valid_twitch,
    "Minecraft": is_valid_minecraft,
    "Steam": is_valid_steam,
}

# --- Twitch OAuth ---
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

# --- Main checker ---
def check_username(username):
    results = {}
    print(f"\n🔍 Checking username: {username}\n")

    # GitHub
    if not is_valid_github(username):
        results["GitHub"] = {"status": "❌ Invalid", "url": None}
    else:
        try:
            url = f"https://api.github.com/users/{username}"
            headers = {"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "username-checker"}
            r = requests.get(url, headers=headers)
            results["GitHub"] = {"status": "❌ Taken", "url": f"https://github.com/{username}"} if r.status_code == 200 else {"status": "✅ Available", "url": None}
        except:
            results["GitHub"] = {"status": "⚠️ Request Failed", "url": None}

    # Steam
    if not is_valid_steam(username):
        results["Steam"] = {"status": "❌ Invalid", "url": None}
    else:
        try:
            url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
            params = {"key": STEAM_API_KEY, "vanityurl": username}
            r = requests.get(url, params=params)
            data = r.json()
            results["Steam"] = {"status": "❌ Taken", "url": f"https://steamcommunity.com/id/{username}"} if data["response"]["success"] == 1 else {"status": "✅ Available", "url": None}
        except:
            results["Steam"] = {"status": "⚠️ Request Failed", "url": None}

    # Roblox
    if not is_valid_roblox(username):
        results["Roblox"] = {"status": "❌ Invalid", "url": None}
    else:
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
    if not is_valid_minecraft(username):
        results["Minecraft"] = {"status": "❌ Invalid", "url": None}
    else:
        try:
            url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
            r = requests.get(url)
            results["Minecraft"] = {"status": "❌ Taken", "url": f"https://namemc.com/profile/{username}"} if r.status_code == 200 else {"status": "✅ Available", "url": None}
        except:
            results["Minecraft"] = {"status": "⚠️ Request Failed", "url": None}

    # Twitch
    if not is_valid_twitch(username):
        results["Twitch"] = {"status": "❌ Invalid", "url": None}
    else:
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
    if not is_valid_tiktok(username):
        results["TikTok"] = {"status": "❌ Invalid", "url": None}
    else:
        try:
            url = f"https://www.tiktok.com/@{username}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            time.sleep(random.uniform(1.5, 3.5))
            r = requests.get(url, headers=headers, timeout=5)
            html = r.text.lower()
            results["TikTok"] = {"status": "❌ Taken", "url": url} if "userinfo" in html else {"status": "✅ Available", "url": None}
        except Exception as e:
            results["TikTok"] = {"status": f"⚠️ Error: {e}", "url": None}

    # Instagram
    if not is_valid_instagram(username):
        results["Instagram"] = {"status": "❌ Invalid", "url": None}
    else:
        try:
            url = f"https://www.instagram.com/{username}/"
            headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X)"}
            time.sleep(random.uniform(1.5, 3.5))
            r = requests.get(url, headers=headers, timeout=5)
            html = r.text.lower()
            results["Instagram"] = {"status": "❌ Taken", "url": url} if "og:image" in html and "og:description" in html else {"status": "✅ Available", "url": None}
        except Exception as e:
            results["Instagram"] = {"status": f"⚠️ Error: {e}", "url": None}

    # YouTube
    if not is_valid_youtube(username):
        results["YouTube"] = {"status": "❌ Invalid", "url": None}
    else:
        try:
            url = f"https://www.youtube.com/@{username}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            results["YouTube"] = {"status": "❌ Taken", "url": url} if r.status_code == 200 else {"status": "✅ Available", "url": None}
        except:
            results["YouTube"] = {"status": "⚠️ Request Failed", "url": None}

    # Facebook
    if not is_valid_facebook(username):
        results["Facebook"] = {"status": "❌ Invalid", "url": None}
    else:
        try:
            url = f"https://www.facebook.com/{username}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5, allow_redirects=True)
            final_url = r.url.lower()
            if r.status_code == 404 or "content isn't available" in r.text.lower() or "page isn't available" in r.text.lower():
                results["Facebook"] = {"status": "✅ Available", "url": None}
            elif username.lower() in final_url.replace(".", ""):
                results["Facebook"] = {"status": "❌ Taken", "url": final_url}
            else:
                results["Facebook"] = {"status": "❌ Taken", "url": final_url}
        except:
            results["Facebook"] = {"status": "⚠️ Request Failed", "url": None}

    # Snapchat
    if not is_valid_snapchat(username):
        results["Snapchat"] = {"status": "❌ Invalid", "url": None}
    else:
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
