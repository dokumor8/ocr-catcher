import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import subprocess

# from rapidocr_onnxruntime import RapidOCR

# engine = RapidOCR(rec_model_path="/common/japanese/ocr/onnx_model/more/japan_PP-OCRv3_rec_infer.onnx")


class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".png"):  # Adjust the file extension if needed
            print("new file found")
            ocr_result = process_image(event.src_path)
            send_to_flask_server(ocr_result)
            # socketio.emit("ocr_result", {"text": ocr_result})


def send_to_flask_server(ocr_result):
    # print(ocr_result)
    url = "http://localhost:5000/upload"
    payload = {"text": ocr_result}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("OCR result sent successfully")
    else:
        print("Failed to send OCR result")


def process_image(image_path):

    result = subprocess.run(
        ["/common/japanese/ocr/onnx_model/PaddleOCR-ONNX-Sample/ocr.sh", image_path],
        capture_output=True,
        text=True,
        cwd="/common/japanese/ocr/onnx_model/PaddleOCR-ONNX-Sample",
    )
    print("subprocess executed")
    # print(result)
    # print(result.stdout)
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
