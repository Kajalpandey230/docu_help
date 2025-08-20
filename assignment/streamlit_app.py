import io
import json
import os
from typing import List, Optional

import streamlit as st
from dotenv import load_dotenv

from src.agent.runner import process_document

load_dotenv()

st.set_page_config(page_title="Document Extraction Agent", page_icon="🧾", layout="wide")

st.title("🧾 Agentic Document Extraction")

with st.sidebar:
	st.header("Settings")
	num_votes = st.slider("Self-consistency votes", min_value=1, max_value=5, value=3)
	temperature = st.slider("LLM temperature", min_value=0.0, max_value=1.2, value=0.2, step=0.1)
	model = st.text_input("OpenAI model", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

uploaded = st.file_uploader("Upload a PDF or image", type=["pdf", "png", "jpg", "jpeg"])

fields_text = st.text_area(
	"Optional: Fields to extract (comma-separated)",
	placeholder="InvoiceNumber, VendorName, Date, TotalAmount",
	height=80,
)

if uploaded is not None:
	st.write("File:", uploaded.name)
	requested_fields: Optional[List[str]] = None
	if fields_text.strip():
		requested_fields = [f.strip() for f in fields_text.split(",") if f.strip()]

	if st.button("Run Extraction", type="primary"):
		with st.spinner("Processing..."):
			try:
				content = uploaded.read()
				result = process_document(
					file_bytes=content,
					filename=uploaded.name,
					requested_fields=requested_fields,
					num_votes=num_votes,
					temperature=temperature,
					model=model,
				)
				st.subheader("Detected Document Type")
				st.info(result.get("doc_type", "unknown"))

				st.subheader("Confidence Scores")
				overall = result.get("overall_confidence", 0.0)
				st.metric("Overall confidence", f"{overall:.2f}")

				fields = result.get("fields", [])
				for fld in fields:
					name = fld.get("name")
					val = fld.get("value")
					conf = float(fld.get("confidence", 0.0))
					col1, col2 = st.columns([2, 5])
					with col1:
						st.caption(name)
						st.write(val)
					with col2:
						st.progress(min(max(conf, 0.0), 1.0), text=f"{conf:.2f}")

				st.subheader("QA / Validation")
				qa = result.get("qa", {})
				passed = qa.get("passed_rules", [])
				failed = qa.get("failed_rules", [])
				notes = qa.get("notes", "")
				st.success(f"Passed: {', '.join(passed) or 'None'}")
				if failed:
					st.error(f"Failed: {', '.join(failed)}")
				if notes:
					st.info(notes)

				st.subheader("Raw JSON Output")
				json_str = json.dumps(result, ensure_ascii=False, indent=2)
				st.code(json_str, language="json")
				st.download_button("Download JSON", data=json_str, file_name="extraction.json", mime="application/json")
			except Exception as exc:
				st.exception(exc) 