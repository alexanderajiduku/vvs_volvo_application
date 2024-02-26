from pydantic import BaseModel, Field, conlist
from typing import List, Optional
import datetime

from pydantic import BaseModel, Field

class CalibrationResponse(BaseModel):
    message: str = Field(..., example="Calibration successful")
    calibration_file_path: str = Field(..., description="The file path to the saved calibration data")
