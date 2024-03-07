# from fastapi import WebSocket, APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database.database import get_db
# from app.shared.shared import height_queue


# router = APIRouter()

# @router.websocket("/ws/heights")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         height = await height_queue.get()  
#         await websocket.send_text(f"Detected height - {height}")

