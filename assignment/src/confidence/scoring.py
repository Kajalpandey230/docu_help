from typing import Dict, List, Any
from ..utils.json_utils import normalize_value, majority_vote, vote_fraction, fuzzy_contains
from ..validation.validators import field_level_validations


def score_fields(votes_per_field: Dict[str, List[str]], ocr_text: str) -> Dict[str, float]:
	scores: Dict[str, float] = {}
	for name, values in votes_per_field.items():
		candidate = majority_vote([normalize_value(v) for v in values])
		vote_conf = vote_fraction(values, candidate)
		ocr_bonus = 1.0 if fuzzy_contains(ocr_text, candidate) else 0.4 if candidate else 0.0
		valid = field_level_validations(name, candidate)
		valid_bonus = 1.0 if valid else 0.0
		conf = 0.5 * vote_conf + 0.3 * ocr_bonus + 0.2 * valid_bonus
		scores[name] = max(0.0, min(1.0, conf))
	return scores


def overall_confidence(field_scores: Dict[str, float], failed_rules: List[str]) -> float:
	if not field_scores:
		return 0.0
	avg = sum(field_scores.values()) / len(field_scores)
	penalty = 0.05 * len(failed_rules)
	return max(0.0, min(1.0, avg - penalty)) 