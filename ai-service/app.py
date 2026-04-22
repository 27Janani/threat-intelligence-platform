from flask import Flask
from services.groq_client import generate_response

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Service Running"

@app.route("/test")
def test():
    try:
        prompt = "Explain AI in simple words"
        result = generate_response(prompt)

        return {
            "status": "success",
            "data": {
                "prompt": prompt,
                "response": result
            },
            "message": "Response generated successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500

if __name__ == "__main__":
    app.run(debug=True)
