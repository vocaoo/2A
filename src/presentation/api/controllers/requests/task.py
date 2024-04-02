from pydantic import BaseModel


class CompleteTaskData(BaseModel):
    near_photo_url: str
    far_photo_url: str
    previous_indication: float
    current_indication: float
