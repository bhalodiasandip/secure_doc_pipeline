# pipeline/pipeline.py
import sys
import traceback
from typing import Any, Dict
from uuid import uuid4, UUID
from datetime import datetime, timezone


from pydantic import ValidationError

from parser.parser import DocumentParser, ParsingError
from models.models import StandardDocumentData


class ProcessingPipeline:
    def __init__(self):
        self._parser = DocumentParser()

    def _log(self, audit_id: str, message: str, level: str = "INFO") -> None:
        """
        Simple audit-style logger: prints an ISO timestamp, audit id, level, and message.
        """
        ts = datetime.now(timezone.utc).isoformat()
        print(f"[{ts}] [{level}] audit_id={audit_id} - {message}")

    def process_document(self, raw_data_string: str, document_name: str) -> Dict[str, Any]:
        """
        Orchestrates parse -> validate -> return model_dump.
        All main work occurs inside a protective try/except/finally as required.
        """
        audit_id = str(uuid4())
        self._log(audit_id, f"START processing document '{document_name}'", "INFO")

        try:
            # Parsing step
            parsed_data = self._parser.parse_output(raw_data_string)
            self._log(audit_id, f"Parsed data successfully. Parsed keys: {list(parsed_data.keys())}", "DEBUG")

            # Attach audit_id into parsed_data (so final validated output includes it)
            parsed_data_with_audit = dict(parsed_data)
            parsed_data_with_audit["audit_id"] = audit_id

            # Validation step - Pydantic will raise ValidationError on invalid data
            validated = StandardDocumentData(**parsed_data_with_audit)

            # Success
            result = validated.model_dump(mode="json")
            if isinstance(result.get("audit_id"), UUID):
                result["audit_id"] = str(result["audit_id"])

            self._log(audit_id, "COMPLETED - Document processed and validated.", "INFO")
            return {
                "status": "COMPLETED",
                "audit_id": str(audit_id),
                "document": result
            }

        except ParsingError as p_err:
            # Log parsing-specific failure
            self._log(audit_id, f"FAILED_PARSING - {p_err}", "ERROR")
            # include traceback for auditability
            tb = traceback.format_exc()
            self._log(audit_id, f"Traceback: {tb}", "ERROR")
            return {"status": "FAILED_PARSING", "audit_id": audit_id, "error": str(p_err)}

        except ValidationError as v_err:
            # Pydantic validation error
            self._log(audit_id, f"FAILED_VALIDATION - {v_err.errors()}", "ERROR")
            tb = traceback.format_exc()
            self._log(audit_id, f"Traceback: {tb}", "ERROR")
            return {"status": "FAILED_VALIDATION", "audit_id": audit_id, "error": v_err.errors()}

        except Exception as exc:
            # Any other unexpected exception
            self._log(audit_id, f"FAILED_UNKNOWN - {exc}", "ERROR")
            tb = traceback.format_exc()
            self._log(audit_id, f"Traceback: {tb}", "ERROR")
            return {"status": "FAILED_UNKNOWN", "audit_id": audit_id, "error": str(exc)}

        finally:
            self._log(audit_id, f"FINISHED processing attempt for '{document_name}'", "INFO")
