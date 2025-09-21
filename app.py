import os
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Klasörler
UPLOAD_DIR = Path("./uploads")
AVATAR_DIR = UPLOAD_DIR / "avatars"
GARMENT_DIR = UPLOAD_DIR / "garments"

AVATAR_DIR.mkdir(parents=True, exist_ok=True)
GARMENT_DIR.mkdir(parents=True, exist_ok=True)

# Statik dosya servisleri (ön izleme için)
app.mount("/static/avatars", StaticFiles(directory=AVATAR_DIR), name="avatars")
app.mount("/static/garments", StaticFiles(directory=GARMENT_DIR), name="garments")

# Sağlık kontrolü
@app.get("/health")
def health():
    return {"status": "ok"}

# Avatar yükleme
@app.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[-1]
        filename = f"{uuid.uuid4()}{ext}"
        file_path = AVATAR_DIR / filename
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return {"status": "success", "filename": filename}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

# Kıyafet yükleme
@app.post("/upload-garment")
async def upload_garment(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[-1]
        filename = f"{uuid.uuid4()}{ext}"
        file_path = GARMENT_DIR / filename
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return {"status": "success", "filename": filename}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

# Kıyafet listeleme
@app.get("/garments")
def list_garments():
    try:
        files = [f"/static/garments/{f.name}" for f in GARMENT_DIR.iterdir() if f.is_file()]
        return {"status": "success", "garments": files}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
