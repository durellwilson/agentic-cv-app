import pytest
import json
import io
from PIL import Image
import numpy as np
from app import app, cv_agent

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_image():
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Agentic Computer Vision' in response.data

def test_upload_image_no_file(client):
    response = client.post('/upload')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_upload_image_success(client, sample_image):
    response = client.post('/upload', data={'image': (sample_image, 'test.jpg')})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'processed_image' in data
    assert 'detections' in data
    assert 'analysis' in data

def test_camera_controls(client):
    # Test start camera
    response = client.get('/start_camera')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'Camera started'
    
    # Test stop camera
    response = client.get('/stop_camera')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'Camera stopped'

def test_cv_agent_initialization():
    assert cv_agent.model is not None
    assert hasattr(cv_agent, 'detect_objects')
    assert hasattr(cv_agent, 'analyze_scene')

def test_scene_analysis():
    detections = [
        {'class': 'person', 'confidence': 0.9},
        {'class': 'car', 'confidence': 0.8}
    ]
    analysis = cv_agent.analyze_scene(detections)
    assert analysis['object_count'] == 2
    assert 'person' in analysis['objects']
    assert analysis['scene_type'] == 'Human Activity'

def test_get_analysis(client):
    response = client.get('/get_analysis')
    assert response.status_code == 200
