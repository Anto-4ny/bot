import express from "express";
import path from "path";
import cors from "cors";
import { Builder, By, Key, until } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome.js"; // ✅ Fix import path
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// ✅ Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ✅ Set EJS as view engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// ✅ Serve static files
app.use(express.static(path.join(__dirname, "public")));

// ✅ Home route to serve index.ejs
app.get("/", (req, res) => {
    res.render("index"); // Ensure "index.ejs" exists inside the "views" folder
});


// ✅ Booking automation using Selenium
const startBooking = async () => {
    let driver;
    try {
        console.log("🚀 Launching Selenium Chrome...");

        // ✅ Configure Chrome options
        const chromeOptions = new chrome.Options();
        chromeOptions.headless(); // Run in headless mode (no UI)
        chromeOptions.addArguments("--no-sandbox");
        chromeOptions.addArguments("--disable-dev-shm-usage");
        chromeOptions.setChromeBinaryPath("/usr/bin/google-chrome-stable"); // ✅ Set Chrome path

        // ✅ Start Selenium WebDriver
        driver = await new Builder()
            .forBrowser("chrome")
            .setChromeOptions(chromeOptions)
            .build();

        console.log("🔗 Opening VFS Global login page...");
        await driver.get("https://visa.vfsglobal.com/sgp/en/prt/login");

        console.log("📄 Navigating to booking page...");
        await driver.get("https://visa.vfsglobal.com/cpv/en/prt/application-detail");

        console.log("📅 Selecting available date...");
        await driver.wait(until.elementLocated(By.css(".available-date")), 10000);
        await driver.findElement(By.css(".available-date")).click();
        await driver.findElement(By.id("continue-button")).click();
        await driver.findElement(By.id("submit-button")).click();

        console.log("✅ Booking completed successfully!");
        return { status: "success", message: "Booking Completed Successfully!" };
    } catch (error) {
        console.error("❌ Booking failed:", error.message);
        return { status: "error", message: error.message };
    } finally {
        if (driver) {
            await driver.quit();
        }
    }
};

// ✅ Booking API route
app.post("/book", async (req, res) => {
    try {
        console.log("📩 Booking request received:", req.body || "No body provided");
        const result = await startBooking();
        res.json(result);
    } catch (error) {
        console.error("❌ Booking API Error:", error.message);
        res.status(500).json({ status: "error", message: "Server error occurred." });
    }
});

// ✅ Start server
app.listen(PORT, () => console.log(`🚀 Server running at http://localhost:${PORT}`));
