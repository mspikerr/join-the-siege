from io import BytesIO

import pytest
from src.app import app, allowed_file

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize("filename, expected", [
    ("file.pdf", True),
    ("file.png", True),
    ("file.jpg", True),
    ("file.txt", True),
    ("file.docx", True),
    ("file.xlsx", True),
    ("file.exe", False),
    ("file", False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected

def test_no_file_in_request(client):
    response = client.post('/classify_file')
    assert response.status_code == 400

def test_no_selected_file(client):
    data = {'file': (BytesIO(b""), '')}  # Empty filename
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"results": [{"error": "No selected file"}]}

def test_success(client, mocker):
    mocker.patch('src.app.classify_file', return_value='test_class')

    data = {
        'file': [
            (BytesIO(b"dummy content 1"), 'file1.pdf'),
            (BytesIO(b"dummy content 2"), 'file2.txt')
        ]
    }
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {
        "results": [
            {"file_name": "file1.pdf", "file_class": "test_class"},
            {"file_name": "file2.txt", "file_class": "test_class"}
        ]
    }