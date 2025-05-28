import requests

def check_username(username):
    sites = {
        "Twitter": f"https://twitter.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
    }

    results = {}
    headers = {"User-Agent": "Mozilla/5.0"}

    for site, url in sites.items():
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 404:
                results[site] = "✅ Available"
            elif response.status_code == 200:
                results[site] = "❌ Taken"
            else:
                results[site] = f"⚠️ Status {response.status_code}"
        except requests.RequestException:
            results[site] = "⚠️ Error"

    return results

if __name__ == "__main__":
    name = input("Enter a username to check: ")
    result = check_username(name)
    for site, status in result.items():
        print(f"{site}: {status}")
