import express from "express";
import path from "path";
import cors from "cors";
import puppeteer from "puppeteer-core";  // ✅ Use "puppeteer-core" for Railway
import chromium from "chrome-aws-lambda"; // ✅ Use "chrome-aws-lambda" to provide Chromium
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

// ✅ Home route
app.get("/", (req, res) => {
    res.render("index");
});

// ✅ Booking automation using Puppeteer
const startBooking = async () => {
    let browser;
    try {
        console.log("🚀 Launching browser...");
        browser = await puppeteer.launch({
            args: chromium.args,
            executablePath: await chromium.executablePath || null, // Removes hardcoded path
            headless: chromium.headless,
            defaultViewport: { width: 1280, height: 800 },
            ignoreHTTPSErrors: true,
        });

        const page = await browser.newPage();
        console.log("🔗 Opening VFS Global login page...");
        await page.goto("https://visa.vfsglobal.com/sgp/en/prt/login", { waitUntil: "networkidle2" });

        console.log("📄 Navigating to booking page...");
        await page.goto("https://visa.vfsglobal.com/cpv/en/prt/application-detail", { waitUntil: "domcontentloaded" });

        console.log("📅 Selecting available date...");
        await page.waitForSelector(".available-date");
        await page.click(".available-date");
        await page.waitForSelector("#continue-button");
        await page.click("#continue-button");
        await page.waitForSelector("#submit-button");
        await page.click("#submit-button");

        console.log("✅ Booking completed successfully!");
        return { status: "success", message: "Booking Completed Successfully!" };
    } catch (error) {
        console.error("❌ Booking failed:", error.message);
        return { status: "error", message: error.message };
    } finally {
        if (browser) {
            await browser.close();
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
