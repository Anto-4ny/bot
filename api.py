from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

def start_booking():
    """Function to automate the visa booking process using Selenium."""
    options = Options()
    options.add_argument("--headless=new")  # ✅ Headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Use correct path for Chrome in Docker
    options.binary_location = "/usr/bin/google-chrome"

    # ✅ Automatically fetch latest ChromeDriver
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
        return {"status": "error", "message": str(e)}
    finally:
        driver.quit()

@app.route("/book", methods=["POST"])
def book():
    """API route to trigger the booking process."""
    print("📩 Booking request received:", request.json)
    result = start_booking()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
