import os
import cv2
import base64
import threading
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from roboflow import Roboflow

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Roboflow model once
rf = Roboflow(api_key="jXhXZWSys4F1FogpsNi6")
project = rf.workspace().project("ppe-wlllw-n9oz8")
model = project.version(1).model

# Global flag to control streaming
streaming = False
stream_lock = threading.Lock()


def run_script(file_path):
    """Run prediction on a single image file."""
    model.predict(file_path, confidence=50, overlap=30).save("prediction.jpg")
    return "Python script has been executed!"


def generate_frames():
    """Generator that yields annotated video frames for streaming."""
    global streaming
    cap = cv2.VideoCapture(0)  # 0 = default webcam

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    try:
        while True:
            with stream_lock:
                if not streaming:
                    break

            success, frame = cap.read()
            if not success:
                break

            # Save frame temporarily for prediction
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_frame.jpg')
            cv2.imwrite(temp_path, frame)

            try:
                # Run PPE prediction on the frame
                prediction = model.predict(temp_path, confidence=50, overlap=30)
                predictions_json = prediction.json()

                # Draw bounding boxes on the frame
                for pred in predictions_json.get('predictions', []):
                    x = int(pred['x'] - pred['width'] / 2)
                    y = int(pred['y'] - pred['height'] / 2)
                    w = int(pred['width'])
                    h = int(pred['height'])
                    label = pred['class']
                    confidence = round(pred['confidence'] * 100, 1)

                    # Color coding: green = PPE detected, red = violation
                    color = (0, 255, 0) if 'vest' in label.lower() or 'helmet' in label.lower() or 'mask' in label.lower() else (0, 0, 255)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(
                        frame,
                        f"{label} {confidence}%",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2
                    )

            except Exception as e:
                # If prediction fails for a frame, just show the raw frame
                cv2.putText(frame, f"Detection error: {str(e)[:40]}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # Encode frame as JPEG for streaming
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:
        cap.release()
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/')
def index():
    return render_template('web2.html')


@app.route('/video-stream')
def video_stream():
    """Route that streams video frames with PPE detection."""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/start-stream', methods=['POST'])
def start_stream():
    global streaming
    with stream_lock:
        streaming = True
    return jsonify({'status': 'streaming started'})


@app.route('/stop-stream', methods=['POST'])
def stop_stream():
    global streaming
    with stream_lock:
        streaming = False
    return jsonify({'status': 'streaming stopped'})


@app.route('/run-script', methods=['GET', 'POST'])
def run_script_route():
    """Upload a single image and run prediction on it."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            result = run_script(file_path)

            # Return the prediction image as base64
            with open("prediction.jpg", "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')

            return jsonify({
                'result': result,
                'prediction_image': f'data:image/jpeg;base64,{img_data}'
            })

    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True, threaded=True)