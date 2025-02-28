from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def extract_alerts(url):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="sso_session",
            headless=True
        )
        page = browser.new_page()
        page.goto(url)

        alert_text = page.inner_text("div.notification-review")  # Example selector
        alert_details = page.inner_text("div.alert-details")

        browser.close()
        return {"alert": alert_text.strip(), "details": alert_details.strip()}

@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json(force=True)  # Ensures JSON is parsed correctly
        if not data or "url" not in data:
            return jsonify({"error": "No URL provided"}), 400

        url = data["url"]
        alert_data = extract_alerts(url)
        return jsonify(alert_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
