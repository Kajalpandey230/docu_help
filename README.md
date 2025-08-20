# 📄 DocuHelp – Intelligent Document Extraction using AI

DocuHelp is an intelligent document processing app that extracts structured data from PDF files or image-based documents using OCR and AI. It converts raw invoices or other documents into clean key-value pairs with confidence scoring and validation — all inside a simple Streamlit interface.

> ⚡ Live Demo: [https://kajalpandey230-docu-help-assignmentstreamlit-app-9xynf6.streamlit.app/](https://kajalpandey230-docu-help-assignmentstreamlit-app-9xynf6.streamlit.app/)

---

## 🧠 Project Overview

This AI-powered tool performs:

- PDF/Image upload
- OCR text extraction
- Document type classification
- Field extraction using GPT models (like GPT-4o)
- Voting-based confidence scoring
- Rule-based validation (like totals matching in invoices)

It is especially useful for tasks like:
- Invoice data extraction
- Automated document processing
- Information retrieval in finance / compliance industries

---

## 🌟 Features

✅ Upload PDFs or images  
✅ Automatic OCR extraction using PyMuPDF / Tesseract  
✅ GPT-based field prediction and JSON output  
✅ Confidence scores for each extracted field  
✅ Clean Streamlit UI  
✅ Deployable on Streamlit Cloud  

---

## 🛠 Tech Stack Used

| Category            | Tools / Libraries                        |
|---------------------|------------------------------------------|
| UI Framework         | Streamlit                               |
| Language             | Python 3                                 |
| OCR                  | PyMuPDF (fitz), PIL                      |
| AI / NLP             | OpenAI GPT models (GPT-4o-mini)          |
| Fuzzy Matching       | RapidFuzz                               |
| Data Processing      | Dataclasses, JSON utils                  |

---

## 🚀 Live Application

You can try the deployed version here:  
👉 **https://kajalpandey230-docu-help-assignmentstreamlit-app-9xynf6.streamlit.app/**

---

## 🧾 How to Run Locally

```bash

# Clone the repo
git clone https://github.com/Kajalpandey230/docu_help.git
cd docu_help/assignment

# Create virtual env (optional)
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# or source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app.py

```

<img width="1898" height="792" alt="image" src="https://github.com/user-attachments/assets/d53731ba-3777-48a2-a6fd-dfb00680ef6f" />

🌈 Future improvements

Add drag-and-drop interface

Support for more document types (receipts, ID cards, etc.)

Add authentication and user history

Docker container / API version for enterprise
