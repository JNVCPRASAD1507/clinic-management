from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MedicalRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    file_name: str
    file_path: str
    file_type: str
    uploaded_at: datetime
