from pydantic import BaseModel


class CameraBase(BaseModel):
    camera_name: str
    camera_model: str
    checkerboard_width: int
    checkerboard_height: int
    description: str


class CameraCreate(CameraBase):
    pass  

class CameraResponse(CameraBase):
    id: int


class CameraList(BaseModel):
    id: int
    camera_name: str
    camera_model: str
    checkerboard_width: int
    checkerboard_height: int
    description: str
    class Config:
        orm_mode = True

