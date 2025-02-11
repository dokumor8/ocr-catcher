from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import json
import os
import sys

# File to store OCR results
OCR_RESULTS_FILE = "ocr_results.json"


def create_app():
    result = subprocess.Popen(
        [sys.executable, "watcher.py"],
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        text=True,  # Use text mode to handle output as strings
        # shell=True  # Use shell to execute the command
    )

    print(result)
    app = Flask(__name__)
    socketio = SocketIO(app)
    return app, socketio


app, socketio = create_app()


def load_ocr_results():
    if not os.path.exists(OCR_RESULTS_FILE):
        return []
    with open(OCR_RESULTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ocr_results(results):
    with open(OCR_RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)


@app.route("/")
def index():
    ocr_results = load_ocr_results()
    recent_results = ocr_results[-50:][::-1]  # Get the 10 most recent results
    print(recent_results)
    print(ocr_results)
    return render_template("index.html", results=recent_results)


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    ocr_results = load_ocr_results()
    recent_results = ocr_results[-50:][::-1]  # Get the 10 most recent results
    emit("ocr_result", {"text": recent_results})


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("update_ocr_result")
def handle_update_ocr_result(data):
    ocr_results = load_ocr_results()
    ocr_results.append(data["text"].strip() + "。\n")
    save_ocr_results(ocr_results)
    print(f'Received OCR result: {data["text"]}')
    recent_results = list(reversed(ocr_results[-50:]))  # Get the 10 most recent results
    emit("ocr_result", {"text": recent_results}, broadcast=True)


if __name__ == "__main__":

    socketio.run(app, debug=True)
