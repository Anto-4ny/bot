import os
import subprocess
from flask import Flask, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

def install_playwright():
    """Ensure Playwright and browsers are installed in Vercel runtime."""
    subprocess.run("playwright install chromium", shell=True, check=True)

def start_booking():
    """Automate visa booking using Playwright."""
    install_playwright()  # Ensure Playwright is installed

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set to False if you want to see browser
        page = browser.new_page()

        try:
            # Open VFS Global login page
            page.goto("https://visa.vfsglobal.com/sgp/en/prt/login")

            # Wait for user to manually log in
            input("Press Enter after logging in...")

            # Navigate to booking page
            page.goto("https://visa.vfsglobal.com/cpv/en/prt/application-detail")

            # Select available date and confirm booking
            page.wait_for_selector(".available-date")
            page.click(".available-date")
            page.click("#continue-button")
            page.click("#submit-button")

            return {"status": "success", "message": "Booking Completed Successfully!"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

        finally:
            browser.close()

@app.route("/api/book", methods=["POST"])
def book():
    result = start_booking()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Run Flask on port 5000
