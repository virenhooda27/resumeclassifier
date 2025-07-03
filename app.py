from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import requests
import os

app = Flask(__name__)
CORS(app)

# ✅ Your IBM Cloud credentials
API_KEY = "ZnuezTFn5SbYDvWa7xAapDX5BA1uemjAnJQ1M6Nowxm6"
DEPLOYMENT_URL = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6ca60c6a-301b-459f-8c3d-7d8017f6ddbd/ai_service?version=2021-05-01"
IAM_URL = "https://iam.cloud.ibm.com/identity/token"

def get_iam_token():
    try:
        print("🔐 Getting IBM IAM access token...")
        response = requests.post(
            IAM_URL,
            data={
                "apikey": API_KEY,
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print("✅ Token response code:", response.status_code)
        response.raise_for_status()
        token = response.json()["access_token"]
        print("✅ Token received!")
        return token
    except Exception as e:
        print("❌ Error getting IAM token:", e)
        raise

def extract_text_from_pdf(file):
    try:
        print("📄 Extracting text from PDF...")
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        print("✅ PDF text extracted. Length:", len(text))
        return text
    except Exception as e:
        print("❌ PDF extraction error:", e)
        raise

@app.route("/")
def home():
    return "✅ Resume Classifier backend is running."

@app.route("/classify", methods=["POST"])
def classify_resume():
    try:
        if "resume" not in request.files:
            print("❌ No file uploaded.")
            return jsonify({"error": "No file uploaded"}), 400

        pdf_file = request.files["resume"]
        print("📎 File received:", pdf_file.filename)

        # 1. Extract and truncate text
        text = extract_text_from_pdf(pdf_file)
        text = text[:4000]

        prompt = f"Classify this text into HR, DS or SDE:\n{text}\n\nOnly output the label."
        print("📤 Prompt ready:\n", prompt[:300], "...")  # Log first 300 chars

        # 2. Get token
        token = get_iam_token()

        # 3. Send to WatsonX
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

        print("🚀 Sending request to WatsonX...")
        response = requests.post(DEPLOYMENT_URL, headers=headers, json=payload)
        print("📬 WatsonX response code:", response.status_code)
        print("📬 WatsonX raw response:", response.text)

        response.raise_for_status()
        result = response.json()
        predicted = result["results"][0]["generated_text"].strip()

        print("✅ Prediction received:", predicted)
        return jsonify({"category": predicted})

    except Exception as e:
        print("❌ Internal server error:", str(e))
        return jsonify({"error": str(e), "category": "Unknown"}), 500

if __name__ == "__main__":
    app.run(debug=True)
