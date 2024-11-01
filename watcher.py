# watcher.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import json
import socketio

# Initialize a Socket.IO client
sio = socketio.Client()


@sio.event
def connect():
    print('Connected to Flask server')


@sio.event
def disconnect():
    print('Disconnected from Flask server')


class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, ocr_script, ocr_cwd):
        self.ocr_script = ocr_script
        self.ocr_cwd = ocr_cwd

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".png"):  # Adjust the file extension if needed
            print(f"Processing {event.src_path}")
            ocr_result = process_image(event.src_path, self.ocr_script, self.ocr_cwd)
            print(ocr_result)
            send_to_flask_server(ocr_result)


def send_to_flask_server(ocr_result):
    sio.emit('update_ocr_result', {'text': ocr_result})


def process_image(image_path, script_path, cwd_path):
    result = subprocess.run(
        [script_path, image_path],
        capture_output=True,
        text=True,
        cwd=cwd_path,
    )
    return result.stdout


if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)
    screenshot_dir = config["screenshots_dir"]
    ocr_script = config["ocr_script"]
    ocr_cwd = config["ocr_cwd"]
    event_handler = ScreenshotHandler(ocr_script, ocr_cwd)
    observer = Observer()
    observer.schedule(event_handler, path=screenshot_dir, recursive=False)
    observer.start()

    time.sleep(5)
    # Connect to the Flask server
    sio.connect('http://localhost:5000')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    sio.disconnect()
