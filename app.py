from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def check_username(username):
    sites = {
        "Twitter": f"https://twitter.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    results = {}

    for site, url in sites.items():
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 404:
                results[site] = "✅ Available"
            elif r.status_code == 200:
                results[site] = "❌ Taken"
            else:
                results[site] = f"⚠️ Status {r.status_code}"
        except:
            results[site] = "⚠️ Error"

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
    app.run(debug=True)
