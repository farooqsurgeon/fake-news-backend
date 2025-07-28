from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # ✅ Allow cross-origin requests from frontend

# ✅ Set up basic logging
logging.basicConfig(level=logging.INFO)

# 🔒 Limit input size to prevent abuse
MAX_TEXT_LENGTH = 5000  # You can adjust this limit

# 🔍 Basic keyword-based prediction logic
def predict_news(text):
    text = text.lower()
    keywords_real = ["government", "official", "report", "confirmed"]
    keywords_fake = ["clickbait", "shocking", "miracle", "you won't believe"]

    real_score = sum(word in text for word in keywords_real)
    fake_score = sum(word in text for word in keywords_fake)

    if fake_score > real_score:
        return "Fake", round(0.6 + 0.1 * fake_score, 2)
    elif real_score > fake_score:
        return "Real", round(0.6 + 0.1 * real_score, 2)
    else:
        return "Real", 0.5  # ⚖️ Default if no keywords matched

# ✅ Prediction endpoint for frontend
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    news_text = data.get('text', '')

    # 🔒 Validate input
    if not news_text or len(news_text) > MAX_TEXT_LENGTH:
        logging.warning("Invalid or too long input received.")
        return jsonify({
            "error": "Invalid or too long input text."
        }), 400

    logging.info(f"Received text: {news_text[:100]}...")  # Log first 100 characters

    prediction, confidence = predict_news(news_text)

    return jsonify({
        "prediction": prediction,
        "confidence": confidence
    })

# 🚀 No need to run app manually on Render
# Remove app.run() block for production deployment
