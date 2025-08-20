from typing import Dict, List, Any
import os

import pytesseract
from PIL import Image


# Auto-set Tesseract path for Windows if not already set
if not os.getenv("TESSERACT_PATH"):
	if os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
		pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
	elif os.path.exists(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"):
		pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
else:
	pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH")


def ocr_pages(images: List[Image.Image]) -> Dict[str, Any]:
	"""Perform OCR on a list of images.

	Returns:
		{"pages": [{"page": i+1, "text": str, "words": [{"text": str, "bbox": [x1,y1,x2,y2]}]}], "full_text": str}
	"""
	pages: List[Dict[str, Any]] = []
	full_text_parts: List[str] = []
	for idx, img in enumerate(images):
		data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
		words = []
		for i in range(len(data["text"])):
			w = data["text"][i]
			if not w or not w.strip():
				continue
			x, y, w_box, h_box = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
			words.append({
				"text": data["text"][i],
				"bbox": [int(x), int(y), int(x + w_box), int(y + h_box)],
			})
		text = pytesseract.image_to_string(img)
		pages.append({"page": idx + 1, "text": text, "words": words})
		full_text_parts.append(text)
	return {"pages": pages, "full_text": "\n".join(full_text_parts)} 