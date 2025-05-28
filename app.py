from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

app = Flask(__name__)

def check_username(username):
    results = {}

    # GitHub (Official API)
    github_url = f"https://api.github.com/users/{username}"
    r = requests.get(github_url)
    if r.status_code == 404:
        results["GitHub"] = "✅ Available"
    elif r.status_code == 200:
        results["GitHub"] = "❌ Taken"
    else:
        results["GitHub"] = f"⚠️ Error ({r.status_code})"

    # Reddit (Public JSON URL)
    reddit_url = f"https://www.reddit.com/user/{username}/about.json"
    r = requests.get(reddit_url, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code == 404:
        results["Reddit"] = "✅ Available"
    elif r.status_code == 200:
        results["Reddit"] = "❌ Taken"
    else:
        results["Reddit"] = f"⚠️ Error ({r.status_code})"

    # Steam (Official API using vanityurl)
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
        results["Steam"] = "⚠️ Error"

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
    port = int(os.environ.get("PORT", 5000))  # For Render or Replit hosting
    app.run(debug=True, host="0.0.0.0", port=port)
