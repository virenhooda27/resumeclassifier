from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import os
import requests

app = Flask(__name__)
CORS(app)  # Allow CORS from any frontend

# Read IBM Watson credentials from environment
WATSON_API_KEY = os.environ.get("WATSON_API_KEY")
WATSON_API_URL = os.environ.get("WATSON_API_URL")  # Should end with /v2/completions

# Extract text from uploaded PDF file
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Send prompt to IBM WatsonX API for classification
def classify_resume_with_ibm(text):
    prompt = f"Classify this resume into one of the following categories: Data Science, Software Development, HR, Design, Marketing.\n\nResume:\n{text[:4000]}"

    headers = {
        "Authorization": f"Bearer {WATSON_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": "granite-3-2-8b-instruct",  # Make sure this is correct
        "input": prompt
    }

    try:
        response = requests.post(WATSON_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("results", [{}])[0].get("generated_text", "No response")
    except Exception as e:
        return f"Error contacting IBM API: {e}"

# POST /classify → Classify uploaded resume
@app.route("/classify", methods=["POST"])
def classify():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["resume"]
    text = extract_text_from_pdf(pdf_file)
    result = classify_resume_with_ibm(text)

    for category in ["Data Science", "Software Development", "HR", "Design", "Marketing"]:
        if category.lower() in result.lower():
            return jsonify({"category": category, "explanation": result})

    return jsonify({"category": "Unknown", "explanation": result})

# Root route to show it's working
@app.route("/")
def home():
    return "✅ Resume Classifier Backend is running."

if __name__ == "__main__":
    app.run(debug=True)
