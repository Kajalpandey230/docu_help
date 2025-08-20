from typing import List, Dict, Any, Optional
import os
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic import BaseModel, Field

from openai import OpenAI

from ..utils.json_utils import safe_json_loads, normalize_value, majority_vote

SYSTEM_PROMPT = (
	"You are an expert document information extraction system. "
	"Given the OCR text of a document and its type, extract key fields. "
	"Return ONLY a JSON object with 'fields' as an array of {name, value}."
)


class ExtractionSchema(BaseModel):
	fields: List[Dict[str, Any]] = Field(default_factory=list)


def build_user_prompt(doc_type: str, ocr_text: str, requested_fields: Optional[List[str]]) -> str:
	base = [
		f"Document type: {doc_type}",
		"Instructions:",
		"- Extract key-value fields typical for this document type.",
		"- If requested fields are provided, prioritize and include them.",
		"- Keep values concise.",
		"- If a field is not found, return an empty string value.",
		"- Do not invent values.",
	]
	if requested_fields:
		base.append("Requested fields: " + ", ".join(requested_fields))
	base.append("OCR text:\n" + ocr_text[:12000])
	base.append("Output JSON shape: {\"fields\": [{\"name\": str, \"value\": str}]}")
	return "\n".join(base)


def demo_extraction(doc_type: str, ocr_text: str, requested_fields: Optional[List[str]]) -> Dict[str, Any]:
	"""Demo extraction without OpenAI API - uses simple heuristics."""
	text_lower = ocr_text.lower()
	fields = []
	
	# Common field patterns
	patterns = {
		"InvoiceNumber": [r"invoice.*?(\d+)", r"inv.*?(\d+)", r"#(\d+)"],
		"Date": [r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})", r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"],
		"TotalAmount": [r"total.*?[\$₹]?\s*([0-9,]+\.?[0-9]*)", r"amount.*?[\$₹]?\s*([0-9,]+\.?[0-9]*)"],
		"VendorName": [r"vendor.*?([a-zA-Z\s]+)", r"company.*?([a-zA-Z\s]+)"],
	}
	
	import re
	for field_name, pattern_list in patterns.items():
		value = ""
		for pattern in pattern_list:
			match = re.search(pattern, text_lower)
			if match:
				value = match.group(1).strip()
				break
		if value:
			fields.append({"name": field_name, "value": value})
	
	# Add requested fields if not found
	if requested_fields:
		for field in requested_fields:
			if not any(f["name"] == field for f in fields):
				fields.append({"name": field, "value": ""})
	
	return {"fields": fields}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def call_openai(prompt: str, model: str, temperature: float) -> Dict[str, Any]:
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key or api_key == "your-openai-api-key-here":
		raise Exception("OpenAI API key not set. Please add your API key to .env file")
	
	client = OpenAI(api_key=api_key)
	resp = client.responses.create(
		model=model,
		input=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
		response_format={
			"type": "json_schema",
			"json_schema": {
				"name": "extraction_schema",
				"schema": {
					"type": "object",
					"properties": {
						"fields": {
							"type": "array",
							"items": {
								"type": "object",
								"properties": {
									"name": {"type": "string"},
									"value": {"type": "string"}
								},
								"required": ["name", "value"]
							}
						}
					},
					"required": ["fields"]
				}
			}
		},
		temperature=temperature,
	)
	content = resp.output[0].content[0].text if resp.output else "{}"
	return safe_json_loads(content)


def extract_fields(doc_type: str, ocr_text: str, requested_fields: Optional[List[str]], num_votes: int, temperature: float, model: str) -> Dict[str, Any]:
	# Check if OpenAI API key is available
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key or api_key == "your-openai-api-key-here":
		# Use demo mode
		data = demo_extraction(doc_type, ocr_text, requested_fields)
		fields = data.get("fields", [])
		final = {f.get("name", ""): normalize_value(f.get("value", "")) for f in fields if f.get("name")}
		votes_per_field = {name: [value] for name, value in final.items()}
		return {"final": final, "votes": votes_per_field}
	
	# Use OpenAI
	prompt = build_user_prompt(doc_type, ocr_text, requested_fields)
	votes: List[Dict[str, str]] = []
	for _ in range(max(1, num_votes)):
		data = call_openai(prompt=prompt, model=model, temperature=temperature)
		fields = data.get("fields", [])
		votes.append({f.get("name", ""): normalize_value(f.get("value", "")) for f in fields if f.get("name")})

	# Build union of field names
	all_names: List[str] = []
	for v in votes:
		for k in v.keys():
			if k not in all_names:
				all_names.append(k)

	# Majority vote values per field
	final: Dict[str, str] = {}
	votes_per_field: Dict[str, List[str]] = {n: [] for n in all_names}
	for name in all_names:
		vals = [normalize_value(v.get(name)) for v in votes if name in v]
		winner = majority_vote(vals)
		final[name] = winner
		votes_per_field[name] = vals

	return {"final": final, "votes": votes_per_field} 