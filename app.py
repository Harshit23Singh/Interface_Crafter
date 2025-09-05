import os
from typing import Any

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from src.llm import generate_guidance
from src.pdf_utils import extract_text_from_pdf
from src.schema import SimplificationRequest, SimplificationResponse


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    CORS(app)

    @app.get("/")
    def index() -> Any:
        return send_from_directory("static", "index.html")

    @app.post("/api/simplify")
    def simplify() -> Any:
        content_type = request.content_type or ""

        if content_type.startswith("multipart/form-data"):
            upload = request.files.get("file")
            if not upload:
                return jsonify({"error": "No file uploaded"}), 400
            if not upload.filename.lower().endswith(".pdf"):
                return jsonify({"error": "Only PDF files are supported"}), 400
            text = extract_text_from_pdf(upload)
            user_prompt = request.form.get("prompt", "")
        else:
            try:
                payload = request.get_json(force=True, silent=False) or {}
            except Exception:
                return jsonify({"error": "Invalid JSON"}), 400
            text = payload.get("text", "")
            user_prompt = payload.get("prompt", "")

        req = SimplificationRequest(text=text, user_prompt=user_prompt)
        if not req.text:
            return jsonify({"error": "Missing text"}), 400

        result: SimplificationResponse = generate_guidance(req)
        return jsonify(result.__dict__), 200

    return app


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    port = int(os.getenv("PORT", "8000"))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)

