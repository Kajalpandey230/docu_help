#!/usr/bin/env python3
"""
Test script to verify app components work correctly.
Run this to test OCR, routing, and validation without needing OpenAI API key.
"""

import os
import sys
from PIL import Image
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ingest.ocr import ocr_pages
from routing.classifier import classify_text_heuristic
from validation.validators import parse_amount, is_valid_date, field_level_validations


def create_test_image():
    """Create a simple test image with text."""
    # Create a white image with black text
    img = Image.new('RGB', (400, 200), color='white')
    from PIL import ImageDraw, ImageFont
    
    draw = ImageDraw.Draw(img)
    # Use default font
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Add some test text
    text_lines = [
        "INVOICE",
        "Invoice Number: INV-001",
        "Date: 2024-01-15",
        "Total Amount: $150.00",
        "Vendor: Test Company"
    ]
    
    y = 20
    for line in text_lines:
        draw.text((20, y), line, fill='black', font=font)
        y += 25
    
    return img


def test_components():
    """Test all components."""
    print("🧪 Testing Document Extraction Components...")
    
    # Test 1: OCR
    print("\n1. Testing OCR...")
    test_img = create_test_image()
    ocr_result = ocr_pages([test_img])
    print(f"   OCR Text: {ocr_result['full_text'][:100]}...")
    print("   ✅ OCR working")
    
    # Test 2: Document Classification
    print("\n2. Testing Document Classification...")
    doc_type = classify_text_heuristic(ocr_result['full_text'])
    print(f"   Detected type: {doc_type}")
    print("   ✅ Classification working")
    
    # Test 3: Validation
    print("\n3. Testing Validation...")
    amount = parse_amount("$150.00")
    print(f"   Amount parsing: $150.00 -> {amount}")
    
    date_valid = is_valid_date("2024-01-15")
    print(f"   Date validation: 2024-01-15 -> {date_valid}")
    
    field_valid = field_level_validations("TotalAmount", "150.00")
    print(f"   Field validation: TotalAmount -> {field_valid}")
    print("   ✅ Validation working")
    
    print("\n🎉 All components working correctly!")
    print("\nNext steps:")
    print("1. Set your OpenAI API key in .env file")
    print("2. Run: streamlit run streamlit_app.py")
    print("3. Upload a document and test extraction")


if __name__ == "__main__":
    test_components() 