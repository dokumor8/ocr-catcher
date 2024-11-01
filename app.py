from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

# Store the latest OCR result
latest_ocr_result = ""


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('ocr_result', {'text': latest_ocr_result})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('update_ocr_result')
def update_ocr_result(result):
    global latest_ocr_result
    latest_ocr_result = result["text"]
    socketio.emit('ocr_result', {'text': latest_ocr_result})


if __name__ == "__main__":
    result = subprocess.run(
        ["./venv/bin/python", "watcher.py"],
    )
    socketio.run(app, debug=True)