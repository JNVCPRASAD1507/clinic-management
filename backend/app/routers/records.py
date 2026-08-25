import os, uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import MedicalRecord, User, UserRole
from app.core.security import get_current_user, require_roles
router=APIRouter(prefix="/medical-records",tags=["Medical Records"])
UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)
ALLOWED={"application/pdf","image/jpeg","image/png"}
@router.post("/upload")
def upload(patient_id:int,file:UploadFile=File(...),db:Session=Depends(get_db),_:User=Depends(require_roles(UserRole.ADMIN,UserRole.DOCTOR,UserRole.RECEPTIONIST))):
    if file.content_type not in ALLOWED:raise HTTPException(400,"Only PDF, JPG and PNG files are supported")
    safe=f"{uuid.uuid4().hex}_{file.filename}"
    path=os.path.join(UPLOAD_DIR,safe)
    with open(path,"wb") as f:f.write(file.file.read())
    obj=MedicalRecord(patient_id=patient_id,file_name=file.filename,file_path=path,content_type=file.content_type);db.add(obj);db.commit();db.refresh(obj)
    return {"id":obj.id,"file_name":obj.file_name,"content_type":obj.content_type}
@router.get("/{patient_id}")
def history(patient_id:int,db:Session=Depends(get_db),_:User=Depends(get_current_user)):
    return db.query(MedicalRecord).filter(MedicalRecord.patient_id==patient_id).order_by(MedicalRecord.uploaded_at.desc()).all()
@router.get("/{patient_id}/download/{record_id}")
def download(patient_id:int,record_id:int,db:Session=Depends(get_db),_:User=Depends(get_current_user)):
    obj=db.get(MedicalRecord,record_id)
    if not obj or obj.patient_id!=patient_id:raise HTTPException(404,"Record not found")
    return FileResponse(obj.file_path,filename=obj.file_name,media_type=obj.content_type)
