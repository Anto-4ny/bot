from flask import Flask, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

def start_booking():
    """Automate visa booking using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use lightweight Chromium
        page = browser.new_page()
        
        # Open VFS Global login page
        page.goto("https://visa.vfsglobal.com/sgp/en/prt/login")
        page.wait_for_load_state("networkidle")

        # Navigate to booking page
        page.goto("https://visa.vfsglobal.com/cpv/en/prt/application-detail")
        page.wait_for_selector(".available-date")

        # Perform booking steps
        page.click(".available-date")
        page.click("#continue-button")
        page.click("#submit-button")

        browser.close()
        return {"status": "success", "message": "Booking Completed Successfully!"}

@app.route("/api/book", methods=["POST"])
def book():
    result = start_booking()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Run Flask on port 5000
