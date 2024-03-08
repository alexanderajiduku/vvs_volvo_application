# import socketio
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.videos import VideoModel
# from app.services.vehicle_measure import VehicleDetectionService
# import os
# from sqlalchemy.future import select



# UPLOAD_DIR = "truckmeasure_uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
# # sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


# @sio.event
# async def vehicle_heights(sid, data):
#     model_id = data.get('model_id')
#     video_id = data.get('video_id')


#     async with AsyncSession() as db_session:
#         video_info = await db_session.execute(
#         select(VideoModel).filter_by(id=video_id, model_id=model_id))
#         video_info = video_info.scalars().first()


#         if video_info:
#             input_source = video_info.file_path
#             vehicle_detection_service = VehicleDetectionService(
#                 model_id=model_id,
#                 db_session=db_session,
#                 output_dir=UPLOAD_DIR,
#                 detected_frames_dir=UPLOAD_DIR
#             )

#             height_data = await vehicle_detection_service.process_video(input_source)

#             for data in height_data:
#                 await sio.emit('height_data', data, to=sid)
#         else:
#             await sio.emit('error', {'message': 'Video information not found for the given video_id.'}, to=sid)
