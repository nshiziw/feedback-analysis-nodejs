from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for a specific origin
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Download necessary NLTK resources
nltk.download('punkt')

# Dummy ML model (replace with a real one later)
# For simplicity, we'll use a random forest classifier to predict satisfaction
X_train = [
    [1, 0],  # positive
    [0, 1],  # negative
    [1, 0],  # positive
    [0, 1]   # negative
]
y_train = [1, 0, 1, 0]  # 1: Satisfied, 0: Unsatisfied

# Train a basic random forest classifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Function to analyze feedback with NLP (tokenizing and counting positive/negative words)
def analyze_feedback(feedback):
    positive_words = ['good', 'great', 'happy', 'excellent', 'amazing']
    negative_words = ['bad', 'poor', 'sad', 'terrible', 'unhappy']
    
    tokens = word_tokenize(feedback.lower())
    positive_count = sum(1 for word in tokens if word in positive_words)
    negative_count = sum(1 for word in tokens if word in negative_words)

    return tokens, positive_count, negative_count

# Function to predict satisfaction using the ML model
def predict_satisfaction(positive_count, negative_count):
    features = np.array([[positive_count, negative_count]])
    prediction = model.predict(features)

    # Map predictions to satisfaction levels and colors
    satisfaction_map = {1: ("Satisfied", "green"), 0: ("Unsatisfied", "red")}
    return satisfaction_map.get(prediction[0], ("Neutral", "blue"))

# Define route to handle feedback analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Parse JSON request
        data = request.get_json()
        feedback = data.get('feedback')

        # Validate feedback input
        if not feedback:
            return jsonify({'error': 'No feedback provided'}), 400

        # Analyze feedback using NLP
        tokens, positive_count, negative_count = analyze_feedback(feedback)

        # Predict satisfaction level
        satisfaction, color = predict_satisfaction(positive_count, negative_count)

        # Return analysis results
        return jsonify({
            'tokens': tokens,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'satisfaction': satisfaction,
            'color': color
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
