from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from PIL import Image

from ..ingest.pdf_utils import pdf_to_images
from ..ingest.ocr import ocr_pages
from ..routing.classifier import classify_text_heuristic
from ..extraction.extractor import extract_fields
from ..validation.validators import totals_match_rule
from ..confidence.scoring import score_fields, overall_confidence


@dataclass
class ProcessOptions:
	num_votes: int = 3
	temperature: float = 0.2
	model: str = "gpt-4o-mini"


def process_document(file_bytes: bytes, filename: str, requested_fields: Optional[List[str]], num_votes: int, temperature: float, model: str) -> Dict[str, Any]:
	is_pdf = filename.lower().endswith(".pdf")
	images: List[Image.Image]
	if is_pdf:
		images = pdf_to_images(file_bytes)
	else:
		# Assume image
		from io import BytesIO
		img = Image.open(BytesIO(file_bytes)).convert("RGB")
		images = [img]

	ocr = ocr_pages(images)
	text = ocr.get("full_text", "")

	doc_type = classify_text_heuristic(text)
	if doc_type == "unknown":
		# default to invoice if ambiguous
		doc_type = "invoice"

	extraction = extract_fields(doc_type, text, requested_fields, num_votes=num_votes, temperature=temperature, model=model)
	final_fields: Dict[str, str] = extraction["final"]
	votes_per_field = extraction["votes"]

	# Confidence per field
	field_scores = score_fields(votes_per_field=votes_per_field, ocr_text=text)

	# QA rules
	passed, failed = [], []
	ok, msg = totals_match_rule(text=text, fields=final_fields) if doc_type == "invoice" else (True, "N/A")
	if ok:
		passed.append("totals_match")
	else:
		failed.append("totals_match")

	overall = overall_confidence(field_scores, failed_rules=failed)

	fields_output = []
	for name, value in final_fields.items():
		fields_output.append({
			"name": name,
			"value": value,
			"confidence": field_scores.get(name, 0.0),
			"source": None,
		})

	return {
		"doc_type": doc_type,
		"fields": fields_output,
		"overall_confidence": overall,
		"qa": {
			"passed_rules": passed,
			"failed_rules": failed,
			"notes": f"{sum(1 for c in field_scores.values() if c < 0.6)} low-confidence fields",
		},
	} 