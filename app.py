from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

# ----------------- DATA STORAGE -----------------
tasks = []
notes = []

# ----------------- ROUTES -----------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", tasks=tasks, notes=notes)

@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        tasks.append(task)
    return jsonify({"tasks": tasks})

@app.route("/delete_task", methods=["POST"])
def delete_task():
    idx = int(request.form.get("index"))
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
    return jsonify({"tasks": tasks})

@app.route("/add_note", methods=["POST"])
def add_note():
    note = request.form.get("note")
    if note:
        notes.append(note)
    return jsonify({"notes": notes})

@app.route("/delete_note", methods=["POST"])
def delete_note():
    idx = int(request.form.get("index"))
    if 0 <= idx < len(notes):
        notes.pop(idx)
    return jsonify({"notes": notes})

@app.route("/timer_tick", methods=["POST"])
def timer_tick():
    # Simple server-side timer placeholder
    return jsonify({"status": "ok"})

# ----------------- RUN APP -----------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)