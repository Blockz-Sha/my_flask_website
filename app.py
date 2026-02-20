from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query_groq', methods=['POST'])
def query_groq():
    query = request.form.get('query')

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    response = requests.get(
        f"https://api.groq.com/query?query={query}",
        headers=headers
    )

    return response.json()

if __name__ == '__main__':
    app.run(debug=True)