# Secure Document Processing Pipeline (Assignment)

## Overview
This project simulates a secure offline pipeline that converts PDF-extracted text/JSON into a validated, standardized JSON schema using Pydantic.

## Structure
- `parser/parser.py` - DocumentParser and ParsingError
- `models/models.py` - Pydantic model `StandardDocumentData`
- `pipeline/pipeline.py` - Orchestration, logging, and error handling
- `run_pipeline.py` - Example execution (success & failure)
- `requirements.txt` - dependencies

## Install
Create and activate your venv, then:
```bash
pip install -r requirements.txt
