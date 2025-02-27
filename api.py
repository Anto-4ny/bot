from flask import Flask, jsonify, render_template
from flask_cors import CORS
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)
CORS(app)  # Allows requests from the frontend

def start_booking():
    driver = uc.Chrome()

    # Open VFS Global login page
    driver.get("https://visa.vfsglobal.com/sgp/en/prt/login")
    time.sleep(10)  # Wait for user to log in manually

    # Wait for user login
    try:
        WebDriverWait(driver, 30).until(EC.url_contains("/dashboard"))
    except:
        return {"status": "error", "message": "Login failed or took too long"}

    # Navigate to booking page
    driver.get("https://visa.vfsglobal.com/cpv/en/prt/application-detail")
    time.sleep(5)

    # Try to book an appointment
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "available-date")))
        driver.find_elements(By.CLASS_NAME, "available-date")[0].click()
        driver.find_element(By.ID, "continue-button").click()
        time.sleep(3)

        driver.find_element(By.ID, "submit-button").click()
        time.sleep(2)

        return {"status": "success", "message": "Booking Completed Successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route("/api/book", methods=["POST"])
def book():
    result = start_booking()
    return jsonify(result)

@app.route("/")
def home():
    return render_template("index.ejs")

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Run Flask on port 5000
