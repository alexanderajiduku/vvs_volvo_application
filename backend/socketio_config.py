import socketio
import logging
from app.services.vehicle_measure import VehicleDetectionService
from app.database.database import SessionLocal

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, environ, auth):
    logger.info(f"Client connected {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected {sid}")

async def process_height_data(vehicle_id, height):
    try:
        logger.info(f"Received height data for vehicle {vehicle_id}: {height}")
    except Exception as e:
        logger.error(f"Error processing height data: {e}")

@sio.event
async def vehicle_height(sid, data):
    try:
        vehicle_id = data.get('id')
        height = data.get('height')
        await process_height_data(vehicle_id, height)
        logger.info(f"Received height data for vehicle {vehicle_id}: {height}")
    except Exception as e:
        logger.error(f"Error processing height data: {e}")

def emit_height_data(data, sid):
     sio.emit('vehicle_height', data, to=sid)

def create_socketio_app(app):
    socketio_app = socketio.ASGIApp(sio, other_asgi_app=app, socketio_path='/socket.io')
    return socketio_app
