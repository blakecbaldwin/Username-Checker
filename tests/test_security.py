import importlib
import os
import re
import unittest
from unittest.mock import patch


os.environ.setdefault("FLASK_DEBUG", "1")
os.environ.setdefault("SECRET_KEY", "test-secret")

app_module = importlib.import_module("app")


class SecurityHardeningTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config.update(TESTING=True)
        app_module._username_cache.clear()

    def _csrf_token(self, html):
        match = re.search(r'name="csrf_token" value="([^"]+)"', html)
        self.assertIsNotNone(match)
        return match.group(1)

    def test_public_routes_render_and_removed_routes_404(self):
        client = app_module.app.test_client()
        for path in ["/", "/about", "/privacy", "/terms", "/contact", "/sitemap.xml"]:
            with self.subTest(path=path):
                response = client.get(path)
                self.assertEqual(response.status_code, 200)
                response.close()

        self.assertEqual(client.get("/banner").status_code, 404)
        self.assertEqual(client.get("/celebrations-data").status_code, 404)

    def test_post_requires_csrf(self):
        client = app_module.app.test_client()
        response = client.post("/", data={"username": "octocat"}, environ_base={"REMOTE_ADDR": "198.51.100.10"})
        self.assertEqual(response.status_code, 400)

    def test_username_rate_limit_after_five_posts(self):
        client = app_module.app.test_client()
        app_module.app.config["WTF_CSRF_ENABLED"] = False
        try:
            with patch.object(app_module, "check_username", return_value={}):
                statuses = [
                    client.post("/", data={"username": "octocat"}, environ_base={"REMOTE_ADDR": "198.51.100.11"}).status_code
                    for _ in range(6)
                ]
        finally:
            app_module.app.config["WTF_CSRF_ENABLED"] = True

        self.assertEqual(statuses[:5], [200, 200, 200, 200, 200])
        self.assertEqual(statuses[5], 429)

    def test_only_api_backed_platforms_are_active(self):
        self.assertEqual(
            set(app_module.platform_checkers.keys()),
            {"Github", "Minecraft", "Reddit", "Roblox", "Steam", "Twitch"},
        )

    def test_username_cache_hits_and_misses(self):
        calls = {"count": 0}

        def validate(username):
            return True

        def check(username):
            calls["count"] += 1
            return {"status": "Available", "url": None}

        original_checkers = app_module.platform_checkers
        app_module.platform_checkers = {"Fake": {"validate": validate, "check": check}}
        try:
            first = app_module.check_username("ExampleUser")
            second = app_module.check_username("exampleuser")
        finally:
            app_module.platform_checkers = original_checkers

        self.assertEqual(calls["count"], 1)
        self.assertEqual(first, second)

    def test_active_platform_missing_credentials_fail_closed(self):
        from platforms import steam, twitch

        with patch.object(steam, "STEAM_API_KEY", None):
            self.assertEqual(steam.check("example")["status"], "Auth Failed")

        with patch.object(twitch, "CLIENT_ID", None), patch.object(twitch, "CLIENT_SECRET", None):
            self.assertEqual(twitch.check("example")["status"], "Auth Failed")


if __name__ == "__main__":
    unittest.main()
