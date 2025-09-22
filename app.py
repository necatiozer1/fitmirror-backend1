import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

# Upload klasörlerini oluştur
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
AVATAR_DIR = UPLOAD_DIR / "avatars"
GARMENT_DIR = UPLOAD_DIR / "garments"

for d in [UPLOAD_DIR, AVATAR_DIR, GARMENT_DIR]:
    d.mkdir(parents=True, exist_ok=True)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...)):
    file_path = AVATAR_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Avatar uploaded successfully", "filename": file.filename}


@app.post("/upload-garment")
async def upload_garment(file: UploadFile = File(...)):
    file_path = GARMENT_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Garment uploaded successfully", "filename": file.filename}


@app.get("/list-garments")
async def list_garments():
    garments = [f.name for f in GARMENT_DIR.iterdir() if f.is_file()]
    return garments
