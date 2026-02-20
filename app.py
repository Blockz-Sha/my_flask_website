from flask import Flask, render_template

app = Flask(__name__)

# Sample data (replace with your storage logic)
tasks = ["Finish homework", "Study math"]
notes = ["Note 1", "Note 2"]

@app.route('/')
def home():
    # Pass tasks and notes directly
    return render_template('index.html', tasks=tasks, notes=notes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)