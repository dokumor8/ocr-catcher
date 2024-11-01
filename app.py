from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

# File to store OCR results
OCR_RESULTS_FILE = "ocr_results.json"


def load_ocr_results():
    if not os.path.exists(OCR_RESULTS_FILE):
        return []
    with open(OCR_RESULTS_FILE, "r") as f:
        return json.load(f)


def save_ocr_results(results):
    with open(OCR_RESULTS_FILE, "w") as f:
        json.dump(results, f)


@app.route("/")
def index():
    ocr_results = load_ocr_results()
    recent_results = reversed(ocr_results[-10:])  # Get the 10 most recent results
    return render_template("index.html", results=recent_results)


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    ocr_results = load_ocr_results()
    recent_results = reversed(ocr_results[-10:])  # Get the 10 most recent results
    emit("ocr_result", {"text": recent_results})


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("update_ocr_result")
def handle_update_ocr_result(data):
    ocr_results = load_ocr_results()
    ocr_results.append(data["text"])
    save_ocr_results(ocr_results)
    print(f'Received OCR result: {data["text"]}')
    recent_results = reversed(ocr_results[-10:])  # Get the 10 most recent results
    emit("ocr_result", {"text": recent_results}, broadcast=True)


if __name__ == "__main__":
    result = subprocess.run(
        ["./venv/bin/python", "watcher.py"],
    )
    socketio.run(app, debug=True)
