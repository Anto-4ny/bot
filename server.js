const express = require("express");
const path = require("path");
const fetch = require("node-fetch");

const app = express();
const PORT = process.env.PORT || 3000;

// Set EJS as view engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Serve static files
app.use(express.static(path.join(__dirname, "public")));

// Home route
app.get("/", (req, res) => {
    res.render("index");
});

// Route to trigger booking API
app.post("/book", async (req, res) => {
    try {
        let response = await fetch("https://your-vercel-domain/api/book", { method: "POST" });
        let data = await response.json();
        res.json(data);
    } catch (error) {
        res.json({ status: "error", message: "Server error: " + error.message });
    }
});

// Start server
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
