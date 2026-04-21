import os
from groq import Groq
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Initialize client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
        