import pytest
from fastapi.testclient import TestClient
from main import app
from dependencies.auth_dependency import get_current_active_user
from models.user import User

# Mock active user
class MockUser(User):
    @classmethod
    def defaults(cls):
        return {
            "id": 1,
            "role": "patient",
            "is_active": True,
            "full_name": "Test Patient",
            "email": "patient@test.com",
        }

async def mock_get_current_active_user():
    return MockUser()

app.dependency_overrides[get_current_active_user] = mock_get_current_active_user

client = TestClient(app)

def test_analyze_scan():
    # We will send a mock file
    file_content = b"fake-image-bytes"
    files = {"file": ("test_scan.png", file_content, "image/png")}

    response = client.post("/api/v1/medical_image/analyze", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert "Mock Image Analysis Report" in json_data["data"]["analysis"]
    assert json_data["data"]["filename"] == "test_scan.png"

def test_interactive_read_mi():
    file_content = b"fake-image-bytes"
    files = {"file": ("test_scan_interactive.png", file_content, "image/png")}
    data = {"prompt": "Is there any anomaly in this MRI scan?"}

    response = client.post("/api/v1/medical_image/interactive", files=files, data=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert "Mock Interactive Image Analysis Report" in json_data["data"]["analysis"]
    assert "Is there any anomaly in this MRI scan?" in json_data["data"]["analysis"]
    assert json_data["data"]["filename"] == "test_scan_interactive.png"
    assert json_data["data"]["prompt"] == "Is there any anomaly in this MRI scan?"
