from typing import Literal
import re

DocType = Literal["invoice", "medical_bill", "prescription", "unknown"]


INVOICE_HINTS = [
	"invoice", "receipt", "total", "balance due", "amount due", "subtotal", "tax", "gst",
]
MEDICAL_BILL_HINTS = [
	"hospital", "admission", "discharge", "patient id", "doctor fee", "room charges", "medical bill",
]
PRESCRIPTION_HINTS = [
	"rx", "prescription", "dosage", "take", "tablet", "mg", "refill", "sig",
]


def classify_text_heuristic(text: str) -> DocType:
	low = text.lower()
	def score(hints):
		return sum(1 for h in hints if h in low)
	s_inv = score(INVOICE_HINTS)
	s_med = score(MEDICAL_BILL_HINTS)
	s_rx = score(PRESCRIPTION_HINTS)
	best = max(s_inv, s_med, s_rx)
	if best == 0:
		return "unknown"
	if best == s_inv:
		return "invoice"
	if best == s_med:
		return "medical_bill"
	return "prescription" 