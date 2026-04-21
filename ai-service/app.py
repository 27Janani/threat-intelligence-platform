from flask import Flask
from services.groq_client import generate_response

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Service Running"

@app.route("/test")
def test():
    result = generate_response("Explain AI in simple words")
    return result

if __name__ == "__main__":
    app.run(debug=True)
    