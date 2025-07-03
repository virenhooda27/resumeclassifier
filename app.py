from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import requests
import os

app = Flask(__name__)
CORS(app)

# ✅ Your actual IBM credentials
API_KEY = "ZnuezTFn5SbYDvWa7xAapDX5BA1uemjAnJQ1M6Nowxm6"
DEPLOYMENT_URL = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6ca60c6a-301b-459f-8c3d-7d8017f6ddbd/ai_service_stream?version=2021-05-01"
IAM_URL = "https://iam.cloud.ibm.com/identity/token"

def get_iam_token():
    response = requests.post(
        IAM_URL,
        data={
            "apikey": API_KEY,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    response.raise_for_status()
    return response.json()["access_token"]

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route("/")
def home():
    return "✅ Resume Classifier backend is running."

@app.route("/classify", methods=["POST"])
def classify_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        # 1. Read and extract text from PDF
        pdf_file = request.files["resume"]
        text = extract_text_from_pdf(pdf_file)
        text = text[:4000]  # truncate to fit within model input limits

        # 2. Build prompt
        prompt = f"Classify this text into HR, DS or SDE:\n{text}\n\nOnly output the label."

        # 3. Get IAM token
        token = get_iam_token()

        # 4. Call WatsonX model
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = requests.post(DEPLOYMENT_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        predicted = result["results"][0]["generated_text"].strip()

        return jsonify({"category": predicted})

    except Exception as e:
        return jsonify({"error": str(e), "category": "Unknown"}), 500

if __name__ == "__main__":
    app.run(debug=True)
