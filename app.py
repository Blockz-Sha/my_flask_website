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

# Initialize the Groq client
APIConfig.init_client()

# ----------------- FLASK APP -----------------
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Get the user message from JSON
    data = request.get_json(force=True)
    user_message = data.get("message", "")

    if not APIConfig.client:
        # If Groq is not available, fallback to simple echo
        reply = f"(Groq not available) You said: {user_message}"
    else:
        try:
            # Call Groq API
            response = APIConfig.client.chat(user_message)
            reply = response.get("reply", f"(No reply) You said: {user_message}")
        except Exception as e:
            reply = f"Error from Groq: {e}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)