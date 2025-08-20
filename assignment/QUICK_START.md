# 🚀 Quick Start Guide

## ✅ **App is Running!**
Your Streamlit app is now running at: **http://localhost:8501**

## 🎯 **How to Use:**

### **Demo Mode (No API Key Required)**
1. Open your browser and go to `http://localhost:8501`
2. Upload any image/PDF from your SROIE dataset
3. The app will automatically extract fields using pattern matching
4. View confidence scores and download JSON results

### **Full Mode (With OpenAI API Key)**
1. Get your OpenAI API key from: https://platform.openai.com/api-keys
2. Edit the `.env` file and replace `your-openai-api-key-here` with your actual key
3. Restart the app: `streamlit run streamlit_app.py`
4. Now you'll get AI-powered extraction with self-consistency voting

## 🎛️ **Settings Explained:**
- **Self-consistency votes**: How many times the AI extracts fields (higher = more accurate but slower)
- **LLM temperature**: Controls randomness (0.0 = very consistent, 1.0 = more creative)
- **OpenAI model**: Which AI model to use (gpt-4o-mini is recommended)

## 📁 **Your Dataset:**
- SROIE dataset is perfect for testing invoices/receipts
- Upload any `.jpg`, `.png`, or `.pdf` file
- The app will auto-detect document type and extract relevant fields

## 🔧 **Troubleshooting:**
- If you get OCR errors, Tesseract is already installed and working
- If you get API errors, make sure your OpenAI key is correct in `.env`
- The app works in demo mode without any API key

## 📊 **Features Working:**
- ✅ Document upload (PDF/PNG/JPG)
- ✅ OCR text extraction
- ✅ Document type detection
- ✅ Field extraction (demo mode)
- ✅ Confidence scoring
- ✅ JSON download
- ✅ Validation rules

**Ready to test! Open http://localhost:8501 in your browser.** 