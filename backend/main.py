import os
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from api.v1.api import api_router
import socketio
from app.database.database import SessionLocal
from app.services.vehicle_measure import VehicleDetectionService
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

UPLOAD_DIR = "truckmeasure_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='http://localhost:3000')
socketio_app = socketio.ASGIApp(sio, other_asgi_app=app)

@sio.event
async def connect(sid, environ, auth):
    logger.info("Client connected", sid)

@sio.event
async def disconnect(sid):
    logger.info("Client disconnected", sid)

@sio.event
async def start_vehicle_detection(sid, data):
    input_source = data.get('input_source')
    model_id = data.get('model_id')
    if not model_id:
        await sio.emit('error', {'message': 'model_id is missing'}, to=sid)
        return
    db_session = SessionLocal()
    try:
        detection_service = VehicleDetectionService(model_id=model_id, db_session=db_session)
        await detection_service.process_video_with_socketio(input_source, sio, sid)
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        await sio.emit('error', {'message': str(e)}, to=sid)
    finally:
        db_session.close()

@app.get("/")
async def home(request: Request):
    return {"message": "Welcome to the home page!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.socketio_app", host="0.0.0.0", port=8000)
