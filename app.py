from playwright.sync_api import sync_playwright
from flask import Flask, request, jsonify

app = Flask(__name__)

def extract_alerts(url):
    try:
        with sync_playwright() as p:
            # Reuse the saved login session
            browser = p.chromium.launch_persistent_context(
                user_data_dir="sso_session",  # Load the previously saved session
                headless=True  # Runs in the background
            )
            page = browser.new_page()
            page.goto(url, timeout=120000)

            # Debugging: Print the page title to confirm we're logged in
            print("🔍 Loaded Page Title:", page.title())

            # Extract alert data (Modify these selectors based on actual HTML structure)
            alert_text = page.inner_text("div.notification-review")
            alert_details = page.inner_text("div.alert-details")

            browser.close()
            return {"alert": alert_text.strip(), "details": alert_details.strip()}
    except Exception as e:
        return {"error": str(e)}

@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json(force=True)
        if not data or "url" not in data:
            return jsonify({"error": "No URL provided"}), 400

        url = data["url"]
        alert_data = extract_alerts(url)
        return jsonify(alert_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
