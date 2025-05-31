import re
import requests

def validate(username):
    return re.fullmatch(r"[a-zA-Z0-9\.]{5,50}", username) is not None

def check(username):
    try:
        url = f"https://www.facebook.com/{username}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5, allow_redirects=True)
        final_url = r.url.lower()
        if r.status_code == 404 or "content isn't available" in r.text.lower() or "page isn't available" in r.text.lower():
            return {"status": "✅ Available", "url": None}
        elif username.lower() in final_url.replace(".", ""):
            return {"status": "❌ Taken", "url": final_url}
        else:
            return {"status": "❌ Taken", "url": final_url}
    except:
        return {"status": "⚠️ Request Failed", "url": None}

facebook_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "5–50 characters. Letters, numbers, and periods only. No underscores or symbols."
}
