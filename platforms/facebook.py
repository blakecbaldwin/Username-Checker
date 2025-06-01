import re
import requests

def validate(username):
    return re.fullmatch(r"[a-zA-Z0-9\.]{5,50}", username) is not None

def check(username):
    try:
        url = f"https://www.facebook.com/{username}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        final_url = r.url.lower()
        html = r.text.lower()

        # Case: clearly not found or invalid page
        if r.status_code == 404 or "content isn't available" in html or "page isn't available" in html:
            return {"status": "Available", "url": None}

        # Heuristic: if the final URL includes the username and no error is shown, it's taken
        normalized = username.lower().replace(".", "")
        if normalized in final_url.replace(".", "") and "content isn't available" not in html:
            return {"status": "Taken", "url": final_url}

        # Fallback if ambiguous
        return {"status": "Available", "url": None}
    except Exception as e:
        return {"status": f"Request Failed: {e}", "url": None}

facebook_checker = {
    "validate": validate,
    "check": check,
    "tooltip": "5–50 characters. Letters, numbers, and periods only. No underscores or symbols."
}