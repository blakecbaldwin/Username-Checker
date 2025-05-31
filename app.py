from flask import Flask, render_template, request
import os
import importlib
import pkgutil
import time
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
app = Flask(__name__)

# Dynamically load all checkers from platforms/ folder
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

# Perform username checks in parallel
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

# Flask Routes
@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    username = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if username:
            results = check_username(username)
    return render_template(
        "index.html",
        username=username,
        results=results,
        platforms=platform_checkers.keys(),
        tooltips=tooltips
    )

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
