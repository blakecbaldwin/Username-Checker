from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import importlib
import os
import pkgutil
import time

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFError, CSRFProtect
import requests

from contact import send_contact_email


load_dotenv()

debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    if debug_mode:
        secret_key = "dev-only-fallback-secret"
    else:
        raise RuntimeError("SECRET_KEY must be set when FLASK_DEBUG is not enabled.")

app = Flask(__name__)
app.secret_key = secret_key
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

csrf = CSRFProtect(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"],
    storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
)

ACTIVE_PLATFORM_MODULES = {"github", "minecraft", "reddit", "roblox", "steam", "twitch"}
DISABLED_PLATFORM_MODULES = {
    "facebook",
    "instagram",
    "pinterest",
    "snapchat",
    "soundcloud",
    "tiktok",
    "youtube",
}
CACHE_TTL_SECONDS = 6 * 60 * 60
CACHE_MAX_ENTRIES = 1000
REQUEST_TIMEOUT = (2, 4)

_username_cache = OrderedDict()


def _render_home_error(message, status_code):
    flash(message, "danger")
    return (
        render_template(
            "index.html",
            username="",
            results={},
            platforms=platform_checkers.keys(),
            tooltips=tooltips,
        ),
        status_code,
    )


@app.errorhandler(413)
def request_too_large(error):
    return _render_home_error("That request was too large. Please shorten your input and try again.", 413)


@app.errorhandler(429)
def rate_limit_exceeded(error):
    return _render_home_error("Too many requests. Please wait a bit before trying again.", 429)


@app.errorhandler(CSRFError)
def csrf_error(error):
    return _render_home_error("Your form session expired. Please refresh the page and try again.", 400)


@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://www.google.com https://www.gstatic.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "font-src 'self' https://cdnjs.cloudflare.com; "
        "img-src 'self' data:; "
        "frame-src https://www.google.com; "
        "connect-src 'self' https://www.google.com"
    )
    return response


@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(".", "sitemap.xml", mimetype="application/xml")


platform_checkers = {}
tooltips = {}
package_dir = os.path.join(os.path.dirname(__file__), "platforms")

for _, module_name, _ in pkgutil.iter_modules([package_dir]):
    if module_name not in ACTIVE_PLATFORM_MODULES:
        continue

    module = importlib.import_module(f"platforms.{module_name}")
    checker_attr = f"{module_name}_checker"
    if hasattr(module, checker_attr):
        checker = getattr(module, checker_attr)
        platform_name = module_name.capitalize()
        platform_checkers[platform_name] = checker
        if "tooltip" in checker:
            tooltips[platform_name] = checker["tooltip"]

print("Loaded active platforms:", list(platform_checkers.keys()))


def normalize_username(username):
    return username.strip().lower()


def _cache_get(platform, username):
    key = (platform.lower(), normalize_username(username))
    cached = _username_cache.get(key)
    if not cached:
        return None

    expires_at, result = cached
    if time.time() >= expires_at:
        _username_cache.pop(key, None)
        return None

    _username_cache.move_to_end(key)
    return result


def _cache_set(platform, username, result):
    key = (platform.lower(), normalize_username(username))
    _username_cache[key] = (time.time() + CACHE_TTL_SECONDS, result)
    _username_cache.move_to_end(key)
    while len(_username_cache) > CACHE_MAX_ENTRIES:
        _username_cache.popitem(last=False)


def check_username(username):
    results = {}
    normalized_username = normalize_username(username)

    def run_check(platform, checker):
        validate_func = checker.get("validate")
        check_func = checker.get("check")
        try:
            if not validate_func(normalized_username):
                return platform, {"status": "Invalid", "url": None}, 0.0

            cached_result = _cache_get(platform, normalized_username)
            if cached_result:
                return platform, cached_result, 0.0

            start = time.time()
            result = check_func(normalized_username)
            duration = time.time() - start
            _cache_set(platform, normalized_username, result)
            return platform, result, duration
        except Exception as exc:
            print(f"{platform} failed: {exc.__class__.__name__}")
            return platform, {"status": "Error", "url": None}, 0.0

    platforms_to_check = list(platform_checkers.items())
    max_workers = min(len(platforms_to_check), 4)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_check, platform, checker) for platform, checker in platforms_to_check]
        for future in as_completed(futures):
            platform, result, duration = future.result()
            print(f"{platform} check took {duration:.2f} seconds")
            results[platform] = result

    return results


@app.context_processor
def inject_now():
    return {"current_year": datetime.now().year}


@app.route("/", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
@limiter.limit("30 per day", methods=["POST"])
def index():
    results = {}
    username = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if len(username) > 50:
            flash("Usernames must be 50 characters or fewer.", "danger")
        elif username:
            results = check_username(username)

    return render_template(
        "index.html",
        username=username,
        results=results,
        platforms=platform_checkers.keys(),
        tooltips=tooltips,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/contact", methods=["GET", "POST"])
@limiter.limit("3 per hour", methods=["POST"])
@limiter.limit("10 per day", methods=["POST"])
def contact():
    recaptcha_site_key = os.getenv("RECAPTCHA_SITE_KEY")

    if request.method == "POST":
        raw_name = request.form.get("name", "")
        raw_email = request.form.get("email", "")
        raw_subject = request.form.get("subject", "")
        raw_message = request.form.get("message", "")
        name = raw_name.strip()
        email = raw_email.strip()
        subject = raw_subject.strip()
        message = raw_message.strip()
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not all([name, subject, message]):
            flash("Please fill out all required fields.", "danger")
        elif any([len(name) > 100, len(email) > 254, len(subject) > 150, len(message) > 4000]):
            flash("One or more fields is too long. Please shorten your message and try again.", "danger")
        elif not recaptcha_response:
            flash("Please complete the reCAPTCHA.", "danger")
        else:
            recaptcha_secret = os.getenv("RECAPTCHA_SECRET_KEY")
            if not recaptcha_secret:
                print("Contact form blocked: missing RECAPTCHA_SECRET_KEY")
                flash("Failed to send message. Please try again later.", "danger")
                return render_template("contact.html", recaptcha_site_key=recaptcha_site_key)

            try:
                verify_resp = requests.post(
                    "https://www.google.com/recaptcha/api/siteverify",
                    data={
                        "secret": recaptcha_secret,
                        "response": recaptcha_response,
                    },
                    timeout=REQUEST_TIMEOUT,
                ).json()
            except requests.RequestException as exc:
                print(f"Contact form blocked: reCAPTCHA verification failed ({exc.__class__.__name__})")
                flash("Failed to send message. Please try again later.", "danger")
                return render_template("contact.html", recaptcha_site_key=recaptcha_site_key)

            if not verify_resp.get("success"):
                flash("reCAPTCHA verification failed.", "danger")
                return render_template("contact.html", recaptcha_site_key=recaptcha_site_key)

            success = send_contact_email(name, email, subject, message)
            if success:
                flash("Message sent successfully!", "success")
                return redirect(url_for("contact"))

            flash("Failed to send message. Please try again later.", "danger")

    return render_template("contact.html", recaptcha_site_key=recaptcha_site_key)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
