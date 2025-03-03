import os
import subprocess
import sys
from flask import Flask, jsonify
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🚀 Flask API is running!"

def install_chrome():
    """Install Chrome based on OS (Windows or Linux)."""
    try:
        if sys.platform.startswith("win"):
            print("🟢 Windows detected: Ensure Chrome is installed manually.")
        else:
            print("🟠 Linux detected: Installing Chrome...")
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "google-chrome-stable"], check=True)
            print("✅ Chrome installed successfully!")
    except Exception as e:
        print(f"❌ Chrome installation failed: {e}")

def start_booking():
    """Automate the booking process using Selenium."""
    install_chrome()  # ✅ Ensure Chrome is installed

    options = Options()
    options.add_argument("--headless")  # ✅ Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Set binary location only if on Linux (Railway)
    if not sys.platform.startswith("win"):
        options.binary_location = "/usr/bin/google-chrome"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("🚀 Launching Selenium Chrome...")
        driver.get("https://visa.vfsglobal.com/sgp/en/prt/login")
        print("🔗 Opened VFS Global login page...")

        driver.get("https://visa.vfsglobal.com/cpv/en/prt/application-detail")
        print("📄 Navigated to booking page...")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".available-date"))).click()
        driver.find_element(By.ID, "continue-button").click()
        driver.find_element(By.ID, "submit-button").click()

        print("✅ Booking completed successfully!")
        return {"status": "success", "message": "Booking Completed Successfully!"}
    except Exception as e:
        print(f"❌ Booking failed: {str(e)}")
        print(traceback.format_exc())
        return {"status": "error", "message": "Internal Server Error", "error": str(e)}
    finally:
        driver.quit()

@app.route("/book", methods=["GET"])  # ✅ Changed to GET
def book():
    """API route to trigger the booking process."""
    print("📩 Booking request received")
    result = start_booking()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
