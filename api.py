import os
import subprocess
import sys
import traceback
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🚀 Flask API is running!"

def install_chrome():
    """Ensure Chrome is installed (Linux only)."""
    try:
        if sys.platform.startswith("win"):
            print("🟢 Windows detected: Ensure Chrome is installed manually.")
        else:
            print("🟠 Linux detected: Installing Chrome...")
            subprocess.run(["apt-get", "update", "-y"], check=True)
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

    print(f"🖥️ Running on: {sys.platform}")
    
    if not sys.platform.startswith("win"):
        options.binary_location = "/usr/bin/google-chrome"
        print(f"🔎 Using Chrome binary: {options.binary_location}")
    else:
        print("🟢 Running on Windows - Chrome must be installed manually.")

    try:
        # ✅ Setup ChromeDriver
        chromedriver_path = ChromeDriverManager().install()
        print(f"🚀 ChromeDriver installed at: {chromedriver_path}")

        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        print("🚀 Launching Selenium Chrome...")
        
        # 1️⃣ Open VFS login page
        driver.get("https://visa.vfsglobal.com/sgp/en/prt/login")
        print("🔗 Opened VFS Global login page...")

        # 2️⃣ Enter login credentials
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "mat-input-0"))).send_keys("your-email@example.com")
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "mat-input-1"))).send_keys("your-password", Keys.RETURN)
            print("✅ Login submitted! Waiting for redirection...")
        except Exception:
            print("❌ Failed to locate login fields. Check website structure.")
            return {"status": "error", "message": "Login fields not found."}

        # 3️⃣ Wait for login success (Modify the element if needed)
        try:
            WebDriverWait(driver, 15).until(EC.url_contains("/application-detail"))
            print("✅ Successfully logged in!")
        except:
            print("❌ Login failed! Check credentials or CAPTCHA.")
            return {"status": "error", "message": "Login failed."}

        # 4️⃣ Navigate to Application Detail page
        driver.get("https://visa.vfsglobal.com/cpv/en/prt/application-detail")
        print("📄 Navigated to booking page...")

        # 5️⃣ Automate booking process
        try:
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".available-date"))).click()
            print("✅ Date selected!")

            driver.find_element(By.ID, "continue-button").click()
            driver.find_element(By.ID, "submit-button").click()
            print("✅ Booking completed successfully!")

            return {"status": "success", "message": "Booking Completed Successfully!"}
        
        except Exception:
            print("❌ Failed to complete booking. Element not found.")
            return {"status": "error", "message": "Booking step failed."}

    except Exception as e:
        print(f"❌ Booking failed: {str(e)}")
        print(traceback.format_exc())
        return {"status": "error", "message": "Internal Server Error", "error": str(e)}

    finally:
        driver.quit()

@app.route("/book", methods=["GET"])
def book():
    """API route to trigger the booking process."""
    print("📩 Booking request received")
    result = start_booking()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
