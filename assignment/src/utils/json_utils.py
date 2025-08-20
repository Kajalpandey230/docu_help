from typing import Any, Dict, List
import json
from rapidfuzz import fuzz


def safe_json_loads(text: str) -> Dict[str, Any]:
	try:
		return json.loads(text)
	except Exception:
		return {}


def normalize_value(val: Any) -> str:
	if val is None:
		return ""
	if isinstance(val, (int, float)):
		return f"{val}"
	return str(val).strip()


def majority_vote(values: List[str]) -> str:
	counts: Dict[str, int] = {}
	for v in values:
		counts[v] = counts.get(v, 0) + 1
	best = sorted(counts.items(), key=lambda x: (-x[1], len(x[0])))[0][0] if counts else ""
	return best


def vote_fraction(values: List[str], winner: str) -> float:
	n = len(values) or 1
	agree = sum(1 for v in values if v == winner)
	return agree / n


def fuzzy_contains(haystack: str, needle: str, threshold: int = 80) -> bool:
	if not needle or not haystack:
		return False
	return fuzz.partial_ratio(needle.lower(), haystack.lower()) >= threshold 