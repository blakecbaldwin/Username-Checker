def check(username):
    try:
        url = f"https://www.reddit.com/user/{username}/about.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; username-checker/1.0)"
        }
        r = requests.get(url, headers=headers, timeout=5)

        # Debug: log status code
        print(f"[Reddit] Status: {r.status_code} for username '{username}'")

        if r.status_code == 200:
            return {"status": "Taken", "url": f"https://www.reddit.com/user/{username}/"}
        elif r.status_code == 404:
            return {"status": "Available", "url": None}
        else:
            return {"status": f"Unknown ({r.status_code})", "url": None}
    except Exception as e:
        print(f"[Reddit] Exception: {e}")
        return {"status": "Request Failed", "url": None}
