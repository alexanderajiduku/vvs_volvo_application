import pytest
from app.services.yolo_services import load_yolo_model

@pytest.mark.asyncio
async def test_load_yolo_model():
    # Test loading the YOLO model with default path
    model = await load_yolo_model()
    assert model is not None
    # Add more assertions or test cases as needed