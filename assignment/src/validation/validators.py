from typing import Dict, Any, List, Tuple
import re
from datetime import datetime

AMOUNT_RE = re.compile(r"[\$₹]?\s?([0-9]{1,3}(?:,[0-9]{3})*|[0-9]+)(?:\.[0-9]{1,2})?")
DATE_RES = [
	re.compile(r"\b(\d{4})[-/](\d{1,2})[-/](\d{1,2})\b"),
	re.compile(r"\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b"),
]


def parse_amount(text: str) -> float:
	match = AMOUNT_RE.search(text or "")
	if not match:
		return 0.0
	val = match.group(0)
	val = val.replace("₹", "").replace("$", "").replace(",", "").strip()
	try:
		return float(val)
	except Exception:
		return 0.0


def is_valid_date(text: str) -> bool:
	if not text:
		return False
	candidates = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y", "%d-%m-%y", "%m-%d-%y", "%d/%m/%y", "%m/%d/%y"]
	for fmt in candidates:
		try:
			datetime.strptime(text.strip(), fmt)
			return True
		except Exception:
			continue
	# As a fallback, attempt regex extraction and re-parse
	for rx in DATE_RES:
		m = rx.search(text)
		if m:
			parts = m.groups()
			joined = "-".join(parts)
			for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%d-%m-%y", "%m-%d-%y"]:
				try:
					datetime.strptime(joined, fmt)
					return True
				except Exception:
					continue
	return False


def totals_match_rule(text: str, fields: Dict[str, Any]) -> Tuple[bool, str]:
	# Try to find line item amounts from text if line items not provided
	# Fallback: if Subtotal and Tax available, check Total ≈ Subtotal + Tax
	total_text = fields.get("TotalAmount") or fields.get("Total") or fields.get("AmountDue")
	subtotal_text = fields.get("Subtotal")
	tax_text = fields.get("Tax")
	total = parse_amount(str(total_text))
	subtotal = parse_amount(str(subtotal_text))
	tax = parse_amount(str(tax_text))
	if total == 0.0:
		return False, "Missing or zero total"
	if subtotal > 0.0 and tax >= 0.0:
		if abs((subtotal + tax) - total) <= max(0.01 * total, 0.5):
			return True, "Totals match"
		return False, "Subtotal + Tax != Total"
	# As a weak heuristic, sum top 3 amounts below total in the text
	amounts = [parse_amount(m) for m in re.findall(AMOUNT_RE, text or "")]
	amounts = [a for a in amounts if a > 0.0 and a <= total]
	amounts.sort(reverse=True)
	approx = sum(amounts[:3])
	if abs(approx - total) <= max(0.05 * total, 1.0):
		return True, "Top amounts sum approx total"
	return False, "No strong totals evidence"


def field_level_validations(field_name: str, value: str) -> bool:
	fname = field_name.lower()
	if any(k in fname for k in ["date", "issued", "invoice date"]):
		return is_valid_date(value)
	if any(k in fname for k in ["amount", "total", "subtotal", "tax", "balance"]):
		return parse_amount(value) > 0.0
	return True 