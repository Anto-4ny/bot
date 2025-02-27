import os
import subprocess
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
CORS(app)

# Install Playwright browsers at runtime (only if missing)
try:
    logging.info("Ensuring Playwright browsers are installed...")
    subprocess.run(["playwright", "install", "chromium"], check=True)
    logging.info("Playwright Chromium installed successfully!")
except Exception as e:
    logging.error(f"Failed to install Playwright browsers: {e}")

def get_chromium_path():
    """Fetch the correct Chromium path for Vercel's serverless environment."""
    base_path = os.getenv("PLAYWRIGHT_BROWSERS_PATH", "/home/sbx_user/.cache/ms-playwright")
    chromium_exec = f"{base_path}/chromium-*/chrome-linux/chrome"

    # Check if Chromium exists
    if os.path.exists(chromium_exec):
        logging.info(f"Using Chromium from: {chromium_exec}")
        return chromium_exec
    else:
        logging.warning("Chromium path not found, using default Playwright installation.")
        return None  # Playwright will use its default

def start_booking():
    """Automate visa booking using Playwright."""
    try:
        with sync_playwright() as p:
            logging.info("Launching browser...")
            browser = p.chromium.launch(
                executable_path=get_chromium_path(),
                headless=True
            )
            page = browser.new_page()

            logging.info("Opening VFS Global login page...")
            page.goto("https://visa.vfsglobal.com/sgp/en/prt/login")
            page.wait_for_load_state("networkidle")

            logging.info("Navigating to booking page...")
            page.goto("https://visa.vfsglobal.com/cpv/en/prt/application-detail")
            page.wait_for_selector(".available-date")

            logging.info("Selecting available date...")
            page.click(".available-date")
            page.click("#continue-button")
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
