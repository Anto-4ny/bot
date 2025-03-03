import express from "express";
import path from "path";
import cors from "cors";
import { fileURLToPath } from "url";
import { dirname } from "path";
import fetch from "node-fetch"; // ✅ Import fetch to communicate with Python API

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const API_URL = process.env.API_URL || "http://localhost:5000"; // ✅ Python API URL

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

// ✅ Booking API route - Calls Python API
app.post("/book", async (req, res) => {
    try {
        console.log("📩 Booking request received:", req.body || "No body provided");

        // ✅ Forward request to Python API
        const response = await fetch(`https://angelic-mindfulness-production.up.railway.app/book`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(req.body)
        });

        const result = await response.json();
        res.json(result);
    } catch (error) {
        console.error("❌ Booking API Error:", error.message);
        res.status(500).json({ status: "error", message: "Server error occurred." });
    }
});

// ✅ Start server
app.listen(PORT, () => console.log(`🚀 Server running at http://localhost:${PORT}`));
