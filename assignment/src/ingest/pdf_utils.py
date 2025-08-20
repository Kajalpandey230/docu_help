from typing import List, Tuple
import io

import fitz  # PyMuPDF
from PIL import Image


def pdf_to_images(pdf_bytes: bytes, dpi: int = 200) -> List[Image.Image]:
	"""Render each PDF page to a PIL Image.

	Args:
		pdf_bytes: Raw PDF bytes
		dpi: Render DPI (higher is slower, more accurate)
	Returns:
		List of PIL Images, one per page
	"""
	doc = fitz.open(stream=pdf_bytes, filetype="pdf")
	images: List[Image.Image] = []
	for page_index in range(len(doc)):
		page = doc.load_page(page_index)
		zoom = dpi / 72.0
		mat = fitz.Matrix(zoom, zoom)
		pix = page.get_pixmap(matrix=mat, alpha=False)
		img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
		images.append(img)
	doc.close()
	return images 