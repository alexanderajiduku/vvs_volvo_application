from fastapi.websockets import WebSocketDisconnect
from fastapi import APIRouter
from app.services.calibration_service import CameraCalibrationService
import pytest
import asyncio
from unittest import mock
from fastapi.testclient import TestClient
from main import app
import logging 

client = TestClient(app)

@pytest.mark.asyncio
@mock.patch('main.VehicleDetectionService')
@mock.patch('main.frames_queue')
async def test_websocket_endpoint(mock_frames_queue, mock_vehicle_detection_service, caplog):
    # Mock the behavior of VehicleDetectionService.stream_video
    mock_video_task = asyncio.Future()
    mock_video_task.set_result(None)
    mock_vehicle_detection_service.stream_video.return_value = mock_video_task

    # Mock the behavior of WebSocket.send_bytes
    mock_websocket = mock.AsyncMock()
    mock_websocket.send_bytes.side_effect = [None, None, WebSocketDisconnect]

    # Make a request to the websocket endpoint
    response = await client.websocket("/ws", subprotocols=["binary"])

    # Assert that the connection was accepted
    assert response.status_code == 101

    # Assert that the input source is logged
    assert "Input source: 0" in caplog.text

    # Assert that frames are sent through the websocket
    assert mock_websocket.send_bytes.call_count == 2

    # Assert that the client disconnect is logged
    assert "Client disconnected" in caplog.text

    # Assert that the cleanup is called
    assert mock_vehicle_detection_service.cleanup.called

    # Assert that the video task is cancelled
    assert mock_video_task.cancel.called
