from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory
import os
import importlib
import pkgutil
import time
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from contact import send_contact_email

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

# Serve sitemap.xml
@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(".", "sitemap.xml", mimetype="application/xml")

# Load platform checkers
platform_checkers = {}
tooltips = {}
package_dir = os.path.join(os.path.dirname(__file__), "platforms")

for _, module_name, _ in pkgutil.iter_modules([package_dir]):
    module = importlib.import_module(f"platforms.{module_name}")
    checker_attr = f"{module_name}_checker"
    if hasattr(module, checker_attr):
        checker = getattr(module, checker_attr)
        platform_name = module_name.capitalize()
        platform_checkers[platform_name] = checker
        if "tooltip" in checker:
            tooltips[platform_name] = checker["tooltip"]

print("Loaded platforms:", list(platform_checkers.keys()))

# Username check logic
def check_username(username):
    results = {}

    def run_check(platform, checker):
        validate_func = checker.get("validate")
        check_func = checker.get("check")
        try:
            if not validate_func(username):
                return platform, {"status": "Invalid", "url": None}, 0.0
            start = time.time()
            result = check_func(username)
            duration = time.time() - start
            return platform, result, duration
        except Exception as e:
            print(f"{platform} failed: {e}")
            return platform, {"status": "Error", "url": None}, 0.0

    platforms_to_check = [
        (platform, checker)
        for platform, checker in platform_checkers.items()
        if platform.lower() != "instagram"
    ]

    max_workers = min(len(platforms_to_check), 10)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_check, platform, checker) for platform, checker in platforms_to_check]
        for future in as_completed(futures):
            platform, result, duration = future.result()
            print(f"{platform} check took {duration:.2f} seconds")
            results[platform] = result

    return results

# Inject year
@app.context_processor
def inject_now():
    return {'current_year': datetime.now().year}

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    username = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if username:
            results = check_username(username)
    return render_template("index.html", username=username, results=results,
                           platforms=platform_checkers.keys(), tooltips=tooltips)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/banner")
def banner():
    return render_template("birthday-anniversary-banner.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    recaptcha_site_key = os.getenv("RECAPTCHA_SITE_KEY")

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not all([name, subject, message]):
            flash("Please fill out all required fields.", "danger")
        elif not recaptcha_response:
            flash("Please complete the reCAPTCHA.", "danger")
        else:
            # Optional: verify reCAPTCHA server-side
            
            import requests
            recaptcha_secret = os.getenv("RECAPTCHA_SECRET_KEY")
            verify_resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
                "secret": recaptcha_secret,
                "response": recaptcha_response
            }).json()
            if not verify_resp.get("success"):
                flash("reCAPTCHA verification failed.", "danger")
                return render_template("contact.html", recaptcha_site_key=recaptcha_site_key)

            success = send_contact_email(name, email, subject, message)
            if success:
                flash("Message sent successfully!", "success")
                return redirect(url_for("contact"))
            else:
                flash("Failed to send message. Please try again later.", "danger")

    return render_template("contact.html", recaptcha_site_key=recaptcha_site_key)

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
