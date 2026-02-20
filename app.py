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
        if Groq is None:
            print("⚠️ Groq library not installed.")
            cls.client = None
            return False
        if not cls.api_key:
            print("⚠️ GROQ_API_KEY not set in environment.")
            cls.client = None
            return False
        try:
            cls.client = Groq(api_key=cls.api_key)
            print("✅ Groq client initialized.")
            return True
        except Exception as e:
            print(f"⚠️ Failed to init Groq client: {e}")
            cls.client = None
            return False


# Initialize Groq client
APIConfig.init_client()

# ----------------- FLASK APP -----------------
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    # Accept JSON or form data
    data = request.get_json() or request.form
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "(No message provided)"}), 400

    if not APIConfig.client:
        # fallback if Groq is not available
        reply = f"(Groq not available) You said: {user_message}"
    else:
        try:
            # Example call to Groq chat API
            result = APIConfig.client.chat(user_message)
            reply = result.get("reply", "No response from Groq")
        except Exception as e:
            reply = f"Error from Groq: {e}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)