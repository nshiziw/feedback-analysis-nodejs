from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Download necessary NLTK resources
nltk.download('punkt')

# Dummy ML model (replace with a real one later)
# For simplicity, we'll use a random forest classifier to predict satisfaction
# Training data: [positive words, negative words] -> [satisfaction]
X_train = [
    [1, 0],  # positive
    [0, 1],  # negative
    [1, 0],  # positive
    [0, 1]   # negative
]
y_train = [1, 0, 1, 0]  # 1: Satisfied, 0: Unsatisfied

# Train a basic random forest classifier (can be replaced with a more advanced model)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Dummy function to analyze feedback with NLP (tokenizing and counting positive/negative words)
def analyze_feedback(feedback):
    positive_words = ['good', 'great', 'happy', 'excellent', 'amazing']
    negative_words = ['bad', 'poor', 'sad', 'terrible', 'unhappy']
    
    tokens = word_tokenize(feedback.lower())
    positive_count = sum(1 for word in tokens if word in positive_words)
    negative_count = sum(1 for word in tokens if word in negative_words)

    return tokens, positive_count, negative_count

# Function to predict satisfaction using ML (simple random forest classifier here)
def predict_satisfaction(positive_count, negative_count):
    features = np.array([[positive_count, negative_count]])
    prediction = model.predict(features)
    
    if prediction == 1:
        return "Satisfied", "green"
    elif prediction == 0:
        return "Unsatisfied", "red"
    else:
        return "Neutral", "blue"

# Define route to handle feedback analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    feedback = data.get('feedback')

    if not feedback:
        return jsonify({'error': 'No feedback provided'}), 400

    # Analyze feedback with NLP
    tokens, positive_count, negative_count = analyze_feedback(feedback)

    # Predict satisfaction with ML
    satisfaction, color = predict_satisfaction(positive_count, negative_count)

    return jsonify({
        'tokens': tokens,
        'satisfaction': satisfaction,
        'color': color
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
