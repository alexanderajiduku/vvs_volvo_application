# from fastapi import WebSocket, APIRouter, WebSocketDisconnect
# from app.shared.shared import frames_queue


# router = APIRouter()

# @router.websocket("/ws")
# async def get_stream(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             frame = await frames_queue.get() 
#             await websocket.send_bytes(frame)  
#     except WebSocketDisconnect:
#         print("Client disconnected")
