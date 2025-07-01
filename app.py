from flask import Flask, render_template, request
import cv2
import numpy as np
import requests
from scene_ocr import describe_scene, run_ocr

ESP32_STREAM_URL = "http://192.168.86.94:81/stream"

app = Flask(__name__)

def fetch_frame_from_stream():
    stream = requests.get(ESP32_STREAM_URL, stream=True)
    bytes_data = b''
    try:
        for chunk in stream.iter_content(chunk_size=1024):
            bytes_data += chunk
            start = bytes_data.find(b'\xff\xd8')  # JPEG start
            end = bytes_data.find(b'\xff\xd9')    # JPEG end
            if start != -1 and end != -1:
                jpg = bytes_data[start:end + 2]
                bytes_data = bytes_data[end + 2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                return frame
    except Exception as e:
        print(f"Error reading from stream: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        task = request.form.get("task")
        frame = fetch_frame_from_stream()
        if frame is None:
            result = "Error: Could not grab frame from ESP32 stream."
        else:
            if task == "scene":
                result = describe_scene(frame)
            elif task == "ocr":
                result = run_ocr(frame)
            else:
                result = "Invalid task."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(threaded=True, debug=True)
