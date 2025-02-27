import express from "express";
import path from "path";
import fetch from "node-fetch";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Set EJS as view engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Serve static files
app.use(express.static(path.join(__dirname, "public")));

// Middleware for JSON and form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Home route
app.get("/", (req, res) => {
    res.render("index");
});
app.use(express.json()); // Ensure JSON body is parsed

app.post("/book", async (req, res) => {
    try {
        console.log("Booking request received:", req.body || "No body provided");

        let response = await fetch("https://bot-six-beige.vercel.app/api/book", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(req.body || {}), // Ensure it sends a valid JSON body
        });

        let data = await response.json();
        res.json(data);
    } catch (error) {
        console.error("Booking API Error:", error);
        res.status(500).json({ status: "error", message: "Server error occurred." });
    }
});


// Start server
app.listen(PORT, () => console.log(`✅ Server running on http://localhost:${PORT}`));
