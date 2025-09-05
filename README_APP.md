Legal Document Simplifier
=========================

Quick start
-----------

1. Create a virtual environment (optional):
   python3 -m venv .venv && source .venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. (Optional) Enable OpenAI integration:
   - Create a .env file (see .env.example)
   - Set OPENAI_API_KEY and OPENAI_MODEL (defaults to gpt-4o-mini)

4. Run the server:
   python app.py

5. Open the app:
   http://localhost:8000

Endpoints
---------

- GET / -> serves the static frontend
- POST /api/simplify (JSON): { "text": string, "prompt": string? }
- POST /api/simplify (form-data with file=PDF, prompt=optional)

Notes
-----

- Without an OPENAI_API_KEY, the app uses a simple fallback summarizer.
- PDF extraction uses pypdf; text quality depends on source PDF.
- This tool is for information only and is not legal advice.

