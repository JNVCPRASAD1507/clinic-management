from datetime import datetime
from pydantic import BaseModel


class MedicalRecordResponse(BaseModel):
    id: int
    patient_id: int
    file_name: str
    file_path: str
    file_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True