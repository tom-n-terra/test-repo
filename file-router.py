from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from models import FileModel  # SQLAlchemy model
from database import get_db  # Dependency to get DB session

router = APIRouter()

class FileInput(BaseModel):
    name: str
    content: str
    is_security_related: Optional[bool] = None

@router.post("/files/")
def create_file(file: FileInput, db: Session = get_db()):
    db_file = FileModel(
        name=file.name,
        content=file.content,
        is_security_related=file.is_security_related
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return {"id": db_file.id, "message": "File stored successfully"}

@router.get("/files/{file_id}")
def get_file(file_id: int, db: Session = get_db()):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
 # Validate file_id is a positive integer to prevent SQL injection
 if file_id <= 0 or not isinstance(file_id, int):
     raise HTTPException(status_code=400, detail="Invalid file_id. Must be a positive integer.")

    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file
