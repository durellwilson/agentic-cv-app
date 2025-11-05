from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import io
from PIL import Image
import threading
import time

app = Flask(__name__)

class CVAgent:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')  # Lightweight YOLO model
        self.camera = None
        self.is_streaming = False
        self.last_detection = {}
        
    def detect_objects(self, frame):
        results = self.model(frame)
        detections = []
        
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    cls = int(box.cls[0].cpu().numpy())
                    
                    if conf > 0.5:
                        detections.append({
                            'class': self.model.names[cls],
                            'confidence': float(conf),
                            'bbox': [int(x1), int(y1), int(x2), int(y2)]
                        })
                        
                        # Draw bounding box
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(frame, f"{self.model.names[cls]} {conf:.2f}", 
                                  (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame, detections
    
    def analyze_scene(self, detections):
        analysis = {
            'object_count': len(detections),
            'objects': [d['class'] for d in detections],
            'high_confidence': [d for d in detections if d['confidence'] > 0.8],
            'timestamp': time.time()
        }
        
        # Simple scene understanding
        if 'person' in analysis['objects']:
            analysis['scene_type'] = 'Human Activity'
        elif any(obj in analysis['objects'] for obj in ['car', 'truck', 'bus']):
            analysis['scene_type'] = 'Traffic Scene'
        elif any(obj in analysis['objects'] for obj in ['dog', 'cat', 'bird']):
            analysis['scene_type'] = 'Animal Scene'
        else:
            analysis['scene_type'] = 'General Scene'
            
        return analysis

cv_agent = CVAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    image = Image.open(file.stream)
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    processed_frame, detections = cv_agent.detect_objects(frame)
    analysis = cv_agent.analyze_scene(detections)
    
    # Convert back to base64 for display
    _, buffer = cv2.imencode('.jpg', processed_frame)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify({
        'processed_image': img_base64,
        'detections': detections,
        'analysis': analysis
    })

@app.route('/start_camera')
def start_camera():
    cv_agent.camera = cv2.VideoCapture(0)
    cv_agent.is_streaming = True
    return jsonify({'status': 'Camera started'})

@app.route('/stop_camera')
def stop_camera():
    cv_agent.is_streaming = False
    if cv_agent.camera:
        cv_agent.camera.release()
    return jsonify({'status': 'Camera stopped'})

def generate_frames():
    while cv_agent.is_streaming and cv_agent.camera:
        success, frame = cv_agent.camera.read()
        if not success:
            break
        
        processed_frame, detections = cv_agent.detect_objects(frame)
        cv_agent.last_detection = cv_agent.analyze_scene(detections)
        
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_analysis')
def get_analysis():
    return jsonify(cv_agent.last_detection)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug, threaded=True)
