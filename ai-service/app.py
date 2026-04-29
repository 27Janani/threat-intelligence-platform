from flask import Flask
from services.groq_client import generate_response
from middleware.input_sanitizer import sanitize_input
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import jsonify
from flask import request

VALID_TOKEN = "secure-token-123"

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

@app.errorhandler(429)
def rate_limit_handler(e):
    return jsonify({
        "status": "error",
        "message": "Too many requests. Please try again later."
    }), 429

@app.route("/")
def home():
    return "AI Service Running"


@app.route("/test", methods=["POST"])
@limiter.limit("30 per minute")
def test():
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header or auth_header != f"Bearer {VALID_TOKEN}":
            return jsonify({
                "status": "error",
                "message": "Unauthorized access"
            }), 401

        #  Get JSON data from user
        data = request.get_json()

        prompt = data.get("prompt", "") if data else ""

        #  Sanitize input
        clean_prompt, error = sanitize_input(prompt)

        if error:
            return jsonify({
                "status": "error",
                "message": error
            }), 400

        #  Call AI
        response = generate_response(clean_prompt)

        return jsonify({
            "status": "success",
            "data": {
                "prompt": clean_prompt,
                "response": response
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.after_request
def secure_headers(response):
    # Strong CSP
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self';"
    )

    # Anti-clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # MIME sniffing protection
    response.headers["X-Content-Type-Options"] = "nosniff"

    # XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Remove server info
    response.headers.pop("Server", None)

    return response

if __name__ == "__main__":
    app.run(debug=True)
