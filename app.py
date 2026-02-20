from flask import Flask, render_template, request, jsonify
import os
import threading
import time
import requests

app = Flask(__name__)

# ----------------- GROQ API -----------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def query_groq(prompt, max_tokens=300):
    if not GROQ_API_KEY:
        return "❌ Groq API key not set!"
    try:
        response = requests.post(
            "https://api.groq.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            }
        )
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ----------------- STORAGE -----------------
notes = []
tasks = []

# ----------------- ROUTES -----------------
@app.route('/')
def home():
    return render_template('index.html', tasks=tasks, notes=notes)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append({"text": task, "done": False})
    return jsonify({"tasks": tasks})

@app.route('/update_task', methods=['POST'])
def update_task():
    idx = int(request.form.get('index'))
    done = request.form.get('done') == 'true'
    tasks[idx]['done'] = done
    return jsonify({"tasks": tasks})

@app.route('/delete_task', methods=['POST'])
def delete_task():
    idx = int(request.form.get('index'))
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
    return jsonify({"tasks": tasks})

@app.route('/add_note', methods=['POST'])
def add_note():
    note = request.form.get('note')
    if note:
        notes.append(note)
    return jsonify({"notes": notes})

@app.route('/delete_note', methods=['POST'])
def delete_note():
    idx = int(request.form.get('index'))
    if 0 <= idx < len(notes):
        notes.pop(idx)
    return jsonify({"notes": notes})

@app.route('/chat', methods=['POST'])
def chat():
    mode = request.form.get('mode')
    user_input = request.form.get('message', '')
    if mode in ["Summarize My Notes", "Help with Notes"] and notes:
        limited_notes = notes[-5:] if len(notes) > 5 else notes
        notes_text = "\n• ".join(limited_notes)
        if mode == "Summarize My Notes":
            prompt = f"Summarize these notes concisely:\n• {notes_text}"
            max_tokens = 300
        else:
            prompt = f"Explain {user_input} based on these notes:\n• {notes_text}"
            max_tokens = 400
    else:
        if mode == "Explain Concept":
            prompt = f"Explain {user_input} in simple terms for a student."
            max_tokens = 300
        elif mode == "Generate Quiz":
            prompt = f"Create 3 multiple choice quiz questions about {user_input}. Include the correct answer."
            max_tokens = 400
        elif mode == "Study Guide":
            prompt = f"Create a study guide for {user_input} with key concepts, important points, and study tips."
            max_tokens = 500
        else:
            prompt = f"Answer this student question helpfully: {user_input}"
            max_tokens = 300

    # Run Groq API in a thread to avoid blocking
    result = query_groq(prompt, max_tokens=max_tokens)
    return jsonify({"response": result})

# ----------------- RUN APP -----------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)