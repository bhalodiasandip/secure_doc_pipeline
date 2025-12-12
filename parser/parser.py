# parser/parser.py
import json
from typing import Any, Dict


class ParsingError(Exception):
    """Raised when the parser fails to convert raw text into JSON/dict."""
    pass


class DocumentParser:
    """
    Simulates the PDF-to-text JSON extraction stage.
    parse_output takes a raw_text string (simulated extractor output) and returns a dict.
    If the raw_text contains the substring "ERROR_BAD_JSON", we simulate a parsing failure.
    """

    def parse_output(self, raw_text: str) -> Dict[str, Any]:
        if "ERROR_BAD_JSON" in raw_text:
            raise ParsingError("Detected ERROR_BAD_JSON marker in input; simulating parser failure.")

        # Try to convert string into a Python dict using json.loads
        try:
            parsed = json.loads(raw_text)
            if not isinstance(parsed, dict):
                raise ParsingError("Parsed JSON is not an object/dictionary.")
            return parsed
        except json.JSONDecodeError as e:
            # Wrap JSON decoding problems in ParsingError for the pipeline to catch
            raise ParsingError(f"JSON decode error: {e.msg}") from e
