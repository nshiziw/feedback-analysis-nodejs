const express = require("express");
const bodyParser = require("body-parser");
const natural = require("natural");
const cors = require("cors"); // Import the cors middleware

const app = express();

// Enable CORS
app.use(cors());

// Middleware
app.use(bodyParser.json());

// Define ML logic for satisfaction prediction
function predictSatisfaction(feedback) {
    const positiveWords = ["good", "excellent", "amazing", "great", "happy"];
    const negativeWords = ["bad", "terrible", "poor", "unhappy", "sad"];

    let score = 0;
    const tokenizer = new natural.WordTokenizer();
    const tokens = tokenizer.tokenize(feedback.toLowerCase());

    tokens.forEach(word => {
        if (positiveWords.includes(word)) score += 1;
        if (negativeWords.includes(word)) score -= 1;
    });

    return score > 0 ? "Satisfied" : score < 0 ? "Unsatisfied" : "Neutral";
}

// API for analyzing feedback
app.post("/analyze", (req, res) => {
    const { feedback } = req.body;

    if (!feedback) {
        return res.status(400).json({ error: "Feedback is required" });
    }

    // Analyze sentiment
    const tokenizer = new natural.WordTokenizer();
    const tokens = tokenizer.tokenize(feedback);

    // Predict satisfaction
    const satisfaction = predictSatisfaction(feedback);

    res.json({
        tokens,
        satisfaction,
    });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
