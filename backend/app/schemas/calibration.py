from pydantic import BaseModel, Field, conlist
from typing import List, Optional
import datetime


class CalibrationResponse(BaseModel):
    message: str = Field(..., example="Calibration successful")
    camera_matrix_path: str = Field(..., description="The file path to the saved camera matrix data")
    dist_coeffs_path: str = Field(..., description="The file path to the saved distortion coefficients data")

