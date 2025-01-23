import { useState } from "react";

function App() {
  const [feedback, setFeedback] = useState("");
  const [result, setResult] = useState(null);

  const analyzeFeedback = async () => {
    if (!feedback) {
      alert("Please enter feedback!");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ feedback }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error analyzing feedback:", error);
    }
  };

  return (
    <div className="App" style={{ padding: "20px" }}>
      <h1>Feedback Analysis</h1>
      <textarea
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        rows="4"
        cols="50"
        placeholder="Enter feedback here..."
        style={{ width: "100%", marginBottom: "10px" }}
      ></textarea>
      <br />
      <button
        onClick={analyzeFeedback}
        style={{
          padding: "10px 20px",
          backgroundColor: "teal",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Analyze Feedback
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Results:</h3>
          <p>
            <strong>Tokens:</strong> {result.tokens.join(", ")}
          </p>
          <p
            style={{
              color: result.color,
              fontWeight: "bold",
              fontSize: "1.2rem",
            }}
          >
            <strong>Satisfaction:</strong> {result.satisfaction}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
