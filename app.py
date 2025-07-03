from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import os
import requests

app = Flask(__name__)

WATSON_API_KEY = os.environ.get("WATSON_API_KEY")
WATSON_API_URL = os.environ.get("WATSON_API_URL")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def classify_resume_with_ibm(text):
    prompt = f"Classify this resume into one of the following categories: Data Science, Software Development, HR, Design, Marketing.\n\nResume:\n{text[:4000]}"

    headers = {
        "Authorization": f"Bearer {WATSON_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": "granite-13b-chat",
        "input": prompt
    }

    response = requests.post(WATSON_API_URL, json=payload, headers=headers)
    result = response.json()
    return result.get("results", [{}])[0].get("generated_text", "No response")

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

if __name__ == "__main__":
    app.run(debug=True)
