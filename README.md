# ocr-catcher

This is a simple OCR wrapper consisting of two parts:

1. Directory watcher to get new screenshots.
2. Flask web app to show the text in a browser window.

Currently I'm using this project for the OCR itself - https://github.com/Kazuhito00/PaddleOCR-ONNX-Sample

The requirement is a script that takes the path to the image as input and writes the OCR result to standard output.
## Running

1. Modify `config.json` to set up paths for your system.
2. Create a virtual environment and install the packages from `requirements.txt`.
3. Run the command `python watcher.py & flask run` in the virtual environment.
