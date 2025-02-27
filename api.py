from flask import Flask, render_template, redirect, url_for
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

def start_booking():
    driver = uc.Chrome()
    
    # 1️⃣ Open VFS Global login page
    driver.get("https://visa.vfsglobal.com/sgp/en/prt/login")
    time.sleep(10)  # Wait for user to log in manually

    # 2️⃣ Detect when user is logged in (check if dashboard appears)
    try:
        WebDriverWait(driver, 30).until(EC.url_contains("/dashboard"))
    except:
        return "Login failed or took too long"

    # 3️⃣ Navigate to booking page
    driver.get("https://visa.vfsglobal.com/cpv/en/prt/application-detail")
    time.sleep(5)

    # 4️⃣ Automate booking (select category, date, confirm)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "available-date")))
        driver.find_elements(By.CLASS_NAME, "available-date")[0].click()
        driver.find_element(By.ID, "continue-button").click()
        time.sleep(3)

        driver.find_element(By.ID, "submit-button").click()
        time.sleep(2)

        return "Booking Completed Successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/api/book")
def book():
    return start_booking()

@app.route("/")
def home():
    return render_template("index.ejs")

if __name__ == "__main__":
    app.run(debug=True)
