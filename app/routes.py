from flask import Blueprint, current_app, jsonify, request
from groq import Groq

from app.database import get_db
from services.ai_service import generate_email

bp = Blueprint("api", __name__)


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.post("/api/email-drafts")
def create_email_draft():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Request body must be a JSON object."), 400

    required_fields = ("audience", "product", "value_proposition")
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify(error="Missing required fields.", fields=missing_fields), 400

    api_key = current_app.config.get("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return jsonify(error="Configure GROQ_API_KEY in your .env file."), 503

    tone = data.get("tone", "professional and conversational")
    try:
        draft = generate_email(
            Groq(api_key=api_key),
            current_app.config["GROQ_MODEL"],
            audience=data["audience"],
            product=data["product"],
            value_proposition=data["value_proposition"],
            tone=tone,
        )
    except Exception:
        current_app.logger.exception("Email draft generation failed")
        return jsonify(error="Email draft generation failed."), 502

    cursor = get_db().execute(
        """
        INSERT INTO email_drafts
            (audience, product, value_proposition, tone, subject, body)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data["audience"],
            data["product"],
            data["value_proposition"],
            tone,
            draft["subject"],
            draft["body"],
        ),
    )
    get_db().commit()

    return jsonify(id=cursor.lastrowid, **draft), 201