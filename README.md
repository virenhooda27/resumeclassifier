# 📄 Resume Screening Assistant

A GenAI-powered web application that automatically classifies resumes into job categories like **SDE**, **DS**, and **HR** using IBM WatsonX Foundation Models.

> 🚀 Built and hosted with [IBM WatsonX](https://www.ibm.com/watsonx), [Render](https://render.com), and [GitHub Pages](https://pages.github.com)

---

## ✨ Features

- ✅ Upload PDF resumes and auto-classify into roles
- 🤖 Uses IBM Granite 3-2-8B Instruct Model via WatsonX
- 🌗 Toggle between Light and Dark Mode
- 📱 Mobile responsive and user-friendly interface
- 🧠 No manual analysis required — AI handles the screening!

---

## 🌐 Live Demo

🔗 **Frontend**: [https://virenhooda27.github.io](https://virenhooda27.github.io)  
🔗 **Backend API**: [https://resumeclassifier.onrender.com/classify](https://resumeclassifier.onrender.com/classify)

> You can upload a `.pdf` resume and instantly get the predicted category!

---

## 🖼️ Screenshots

### 🖥️ Main Interface
<!-- Replace this with your actual screenshot -->
![Homepage Screenshot](https://github.com/virenhooda27/resumeclassifier/blob/main/Screenshot%202025-07-03%20182753.png?raw=true)


### 📤 Resume Upload
<!-- Replace this with your actual screenshot -->
![Upload Resume](https://github.com/virenhooda27/resumeclassifier/blob/c7b482c070a58649c5e701a360e54d9076860820/Screenshot%202025-07-03%20182802.png)

### 📊 Prediction Result
<!-- Replace this with your actual screenshot -->
![Predicted Category](https://github.com/virenhooda27/resumeclassifier/blob/c7b482c070a58649c5e701a360e54d9076860820/Screenshot%202025-07-03%20182849.png)

---

## 🧠 Powered By

- 🔹 **IBM WatsonX** `granite-3-2-8b-instruct`
- 🔹 **Flask** (Python)
- 🔹 **Render** (for backend deployment)
- 🔹 **GitHub Pages** (for frontend hosting)
- 🔹 **PyMuPDF** for PDF text extraction

---

## 🛠️ How to Run Locally

### 📦 Backend (Flask)
```bash
git clone https://github.com/yourusername/resume-classifier.git
cd resume-classifier
pip install -r requirements.txt
python app.py
