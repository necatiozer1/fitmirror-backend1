import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models import Avatar, Garment

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_avatar(file: UploadFile, db: Session):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    avatar = Avatar(user_id=1, file_path=file_path)
    db.add(avatar)
    db.commit()
    return {"message": "Avatar uploaded", "file_path": file_path}

def save_garment(file: UploadFile, db: Session):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    garment = Garment(user_id=1, file_path=file_path)
    db.add(garment)
    db.commit()
    return {"message": "Garment uploaded", "file_path": file_path}

def try_on(user_id: int, db: Session):
    avatar = db.query(Avatar).filter(Avatar.user_id == user_id).first()
    garment = db.query(Garment).filter(Garment.user_id == user_id).first()
    if not avatar or not garment:
        return {"error": "Avatar or Garment missing"}
    return {
        "message": f"User {user_id} trying on garment",
        "avatar": avatar.file_path,
        "garment": garment.file_path,
    }
