import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from flask_socketio import send, emit
from app import socketio  # Import the SocketIO instance from your Flask app


class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".png"):  # Adjust the file extension if needed
            ocr_result = process_image(event.src_path)
            socketio.emit("ocr_result", {"text": ocr_result})


def process_image(image_path):
    result = subprocess.run(["rapidocr", image_path], capture_output=True, text=True)
    return result.stdout


if __name__ == "__main__":
    screenshot_dir = "/common/japanese/ocr/screenshots/"
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, path=screenshot_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
