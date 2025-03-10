import express from "express";
import path from "path";
import cors from "cors";
import { fileURLToPath } from "url";
import { dirname } from "path";
import fetch from "node-fetch"; // ✅ Import fetch

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

// ✅ Booking API route - Calls Python API using GET
app.get("/book", async (req, res) => {
    try {
        console.log("📩 Booking request received");

        // ✅ Forward request to Python API using GET
        const response = await fetch(`${API_URL}/book`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        res.json(result);
    } catch (error) {
        console.error("❌ Booking API Error:", error.message);
        res.status(500).json({ status: "error", message: "Server error occurred." });
    }
});

// ✅ Start server
app.listen(PORT, () => console.log(`🚀 Server running at http://localhost:${PORT}`));
