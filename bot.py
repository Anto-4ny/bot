import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Function to introduce random delays
def random_sleep(a=2, b=5):
    time.sleep(random.uniform(a, b))

# Set up undetected ChromeDriver
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
options.add_argument("--incognito")  # Use incognito mode
options.add_argument("--start-maximized")  # Start maximized
driver = uc.Chrome(options=options)

# Credentials
EMAIL = "qatrtarikprt01@mailsac.com"
PASSWORD = "@T147852a#@"

def login():
    driver.get("https://visa.vfsglobal.com/sgp/en/prt/login")  
    random_sleep(3, 6)

    try:
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password = driver.find_element(By.NAME, "password")

        # Type like a human
        for char in EMAIL:
            username.send_keys(char)
            random_sleep(0.1, 0.3)  

        for char in PASSWORD:
            password.send_keys(char)
            random_sleep(0.1, 0.3)

        password.send_keys(Keys.RETURN)
        print("Logging in...")

        # Wait for successful login
        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        print("Login successful")

    except Exception as e:
        print(f"Error during login: {e}")

def book_appointment():
    try:
        driver.get("https://visa.vfsglobal.com/ago/en/prt/application-detail")
        random_sleep(3, 6)

        # Select application category
        category_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "category"))
        )
        category_dropdown.click()
        random_sleep(1, 3)
        category_dropdown.send_keys("Job Vacancy")  # Adjust based on actual options
        category_dropdown.send_keys(Keys.RETURN)

        # Check for available dates
        dates = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "available-date"))
        )

        if dates:
            dates[0].click()  # Select the first available date
            print("Date selected")
        else:
            print("No available dates, try again later.")
            return

        # Click continue
        driver.find_element(By.ID, "continue-button").click()
        random_sleep(2, 4)

        # Submit the form
        driver.find_element(By.ID, "submit-button").click()
        random_sleep(2, 4)

        # Handle OTP verification
        otp_attempts = 0
        while otp_attempts < 3:
            otp = input("Enter the OTP received via email: ")
            if otp:
                break
            otp_attempts += 1
            print("Invalid OTP. Try again.")

        if otp_attempts == 3:
            print("Too many failed OTP attempts. Exiting.")
            return

        # Confirm booking
        driver.find_element(By.ID, "confirm-button").click()
        print("Appointment booked successfully")

    except Exception as e:
        print(f"Error during booking: {e}")

def main():
    login()
    book_appointment()
    driver.quit()

if __name__ == "__main__":
    main()
