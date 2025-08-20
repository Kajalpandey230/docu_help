from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SourceBBox(BaseModel):
	x1: int
	y1: int
	x2: int
	y2: int


class FieldItem(BaseModel):
	name: str
	value: Optional[str] = None
	confidence: float = 0.0
	source: Optional[Dict[str, Any]] = None


class ExtractionResult(BaseModel):
	doc_type: str
	fields: List[FieldItem] = Field(default_factory=list)
	overall_confidence: float = 0.0
	qa: Dict[str, Any] = Field(default_factory=dict)

	def to_json(self) -> Dict[str, Any]:
		return self.model_dump() 