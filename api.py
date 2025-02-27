import subprocess
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Ensure Playwright browsers are installed
try:
    subprocess.run(["playwright", "install", "chromium"], check=True)
except Exception as e:
    logging.error(f"Failed to install Playwright browsers: {e}")

def start_booking():
    """Automate visa booking using Playwright."""
    try:
        with sync_playwright() as p:
            logging.info("Launching browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Open VFS Global login page
            logging.info("Opening VFS Global login page...")
            page.goto("https://visa.vfsglobal.com/sgp/en/prt/login")
            page.wait_for_load_state("networkidle")

            # Navigate to booking page
            logging.info("Navigating to booking page...")
            page.goto("https://visa.vfsglobal.com/cpv/en/prt/application-detail")
            page.wait_for_selector(".available-date")

            # Perform booking steps
            logging.info("Selecting available date...")
            page.click(".available-date")

            logging.info("Clicking continue button...")
            page.click("#continue-button")

            logging.info("Submitting booking...")
            page.click("#submit-button")

            browser.close()
            logging.info("Booking completed successfully!")

            return {"status": "success", "message": "Booking Completed Successfully!"}

    except Exception as e:
        logging.error(f"Booking failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running!"})

@app.route("/api/book", methods=["POST"])
def book():
    result = start_booking()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
