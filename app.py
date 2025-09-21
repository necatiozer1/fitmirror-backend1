import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# FastAPI uygulaması
app = FastAPI()

# CORS (Xcode'dan API çağrılarını engellemesin diye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Klasörleri hazırla
BASE_DIR = Path(__file__).resolve().parent
STORAGE = BASE_DIR / "storage"
AVATARS = STORAGE / "avatars"
GARMENTS = STORAGE / "garments"

os.makedirs(AVATARS, exist_ok=True)
os.makedirs(GARMENTS, exist_ok=True)

# Sağlık kontrolü
@app.get("/health")
def health():
    return {"status": "ok"}

# Avatar yükleme
@app.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...)):
    file_path = AVATARS / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": "Avatar uploaded successfully", "filename": file.filename}

# Kıyafet yükleme
@app.post("/upload-garment")
async def upload_garment(file: UploadFile = File(...)):
    file_path = GARMENTS / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": "Garment uploaded successfully", "filename": file.filename}

# Kıyafetleri listeleme
@app.get("/list-garments")
def list_garments():
    garments = [f.name for f in GARMENTS.glob("*") if f.is_file()]
    return garments
