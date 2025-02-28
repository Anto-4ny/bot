import express from "express";
import path from "path";
import cors from "cors"; // ✅ Added CORS support
import fetch from "node-fetch";
import puppeteer from "puppeteer";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// ✅ Middleware
app.use(cors()); // Allow cross-origin requests
app.use(express.json()); // Parse JSON request bodies
app.use(express.urlencoded({ extended: true })); // Parse form data

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
    try {
        console.log("🚀 Launching browser...");
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();

        console.log("🔗 Opening VFS Global login page...");
        await page.goto("https://visa.vfsglobal.com/sgp/en/prt/login", { waitUntil: "networkidle2" });

        console.log("📄 Navigating to booking page...");
        await page.goto("https://visa.vfsglobal.com/cpv/en/prt/application-detail", { waitUntil: "domcontentloaded" });

        console.log("📅 Selecting available date...");
        await page.waitForSelector(".available-date");
        await page.click(".available-date");
        await page.click("#continue-button");
        await page.click("#submit-button");

        await browser.close();
        console.log("✅ Booking completed successfully!");
        return { status: "success", message: "Booking Completed Successfully!" };
    } catch (error) {
        console.error("❌ Booking failed:", error.message);
        return { status: "error", message: error.message };
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
