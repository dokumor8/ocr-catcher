from flask import Flask, request, jsonify, render_template
import subprocess
import requests

app = Flask(__name__)

# Store the latest OCR result
latest_ocr_result = ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    global latest_ocr_result
    latest_ocr_result = request.json.get("text", "")
    return jsonify({"status": "success"})


@app.route("/get_ocr_result", methods=["GET"])
def get_ocr_result():
    return jsonify({"text": latest_ocr_result})


if __name__ == "__main__":
    result = subprocess.run(
        ["./venv/bin/python", "watcher.py"],
    )
    app.run(debug=True)
