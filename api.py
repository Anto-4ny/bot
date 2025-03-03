from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

app = Flask(__name__)

def start_booking(browser="chrome"):
    """Automates booking on VFS Global based on selected browser."""
    driver = None
    
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless=new")  # ✅ Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("--headless=new")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

    else:
        return {"status": "error", "message": f"Unsupported browser: {browser}"}

    try:
        print(f"🚀 Launching Selenium in {browser}...")

        driver.get("https://visa.vfsglobal.com/sgp/en/prt/login")
        print("🔗 Opened VFS Global login page...")

        driver.get("https://visa.vfsglobal.com/cpv/en/prt/application-detail")
        print("📄 Navigated to booking page...")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".available-date"))).click()
        driver.find_element(By.ID, "continue-button").click()
        driver.find_element(By.ID, "submit-button").click()

        print("✅ Booking completed successfully!")
        return {"status": "success", "message": f"Booking Completed Successfully on {browser}!"}

    except Exception as e:
        print(f"❌ Booking failed on {browser}: {str(e)}")
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()

@app.route("/book", methods=["POST"])
def book():
    """API route to trigger the booking process."""
    data = request.json
    browser = data.get("browser", "chrome")  # Default to Chrome if no browser is specified
    print(f"📩 Booking request received for {browser}")
    
    result = start_booking(browser)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
