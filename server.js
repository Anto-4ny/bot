import express from "express";
import path from "path";
import cors from "cors"; // ✅ Added CORS support
import fetch from "node-fetch";
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

// ✅ Booking API route
app.post("/book", async (req, res) => {
    try {
        console.log("📩 Booking request received:", req.body || "No body provided");

        const response = await fetch("https://bot-six-beige.vercel.app/api/book", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(req.body || {}), // Ensure valid JSON body
        });

        if (!response.ok) {
            throw new Error(`API responded with status ${response.status}`);
        }

        const data = await response.json();
        console.log("✅ Booking response:", data);
        res.json(data);
    } catch (error) {
        console.error("❌ Booking API Error:", error.message);
        res.status(500).json({ status: "error", message: "Server error occurred." });
    }
});

// ✅ Start server
app.listen(PORT, () => console.log(`🚀 Server running at http://localhost:${PORT}`));
