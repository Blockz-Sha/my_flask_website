import os
from flask import Flask, request, jsonify, render_template

# ----------------- GROQ API -----------------
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    Groq = None
    GROQ_AVAILABLE = False

API_KEY = os.environ.get("GROQ_API_KEY")

class APIConfig:
    api_key = API_KEY
    client = None

    @classmethod
    def init_client(cls):
        if Groq is None or cls.api_key is None:
            cls.client = None
            return False
        try:
            cls.client = Groq(api_key=cls.api_key)
            return True
        except Exception as e:
            print(f"⚠️ Failed to init Groq client: {e}")
            cls.client = None
            return False

# Initialize client
APIConfig.init_client()

# ----------------- FLASK APP -----------------
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    
    if not APIConfig.client:
        # fallback if Groq is not available
        reply = f"(Groq not available) You said: {user_message}"
    else:
        try:
            result = APIConfig.client.chat(user_message)  # Example Groq call
            reply = result.get("reply", "No response")
        except Exception as e:
            reply = f"Error from Groq: {e}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)