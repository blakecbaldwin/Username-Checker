from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app = Flask(__name__)

def check_username(username):
    results = {}

    # GitHub API with authentication
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

    # Reddit check with enhanced headers
    reddit_url = f"https://www.reddit.com/user/{username}/about.json"
    reddit_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
    try:
        r = requests.get(reddit_url, headers=reddit_headers)
        if r.status_code == 404:
            results["Reddit"] = "✅ Available"
        elif r.status_code == 200:
            results["Reddit"] = "❌ Taken"
        else:
            results["Reddit"] = f"⚠️ Error ({r.status_code})"
    except:
        results["Reddit"] = "⚠️ Request Failed"

    # Steam API
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
    port = int(os.environ.get("PORT", 5000))  # For local or Render
    app.run(debug=False, host="0.0.0.0", port=port)
