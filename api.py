from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

def start_booking():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without GUI (important for Vercel)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)  

    try:
        # Open VFS Global login page
        driver.get("https://visa.vfsglobal.com/sgp/en/prt/login")
        time.sleep(10)  # Wait for user to log in manually

        # Wait for user login
        WebDriverWait(driver, 30).until(EC.url_contains("/dashboard"))

        # Navigate to booking page
        driver.get("https://visa.vfsglobal.com/cpv/en/prt/application-detail")
        time.sleep(5)

        # Try to book an appointment
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "available-date")))
        driver.find_elements(By.CLASS_NAME, "available-date")[0].click()
        driver.find_element(By.ID, "continue-button").click()
        time.sleep(3)

        driver.find_element(By.ID, "submit-button").click()
        time.sleep(2)

        return {"status": "success", "message": "Booking Completed Successfully!"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()  # Ensure Chrome closes after booking

@app.route("/api/book", methods=["POST"])
def book():
    result = start_booking()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Run Flask on port 5000
