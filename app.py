import os
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from PIL import Image

app = FastAPI()

# Klasörler
STORAGE = Path("./storage").resolve()
AVATARS = STORAGE / "avatars"
GARMENTS = STORAGE / "garments"
RESULTS = STORAGE / "results"

for folder in [AVATARS, GARMENTS, RESULTS]:
    folder.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...)):
    filename = f"avatar_{uuid.uuid4().hex}{Path(file.filename).suffix}"
    file_path = AVATARS / filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": "Avatar uploaded successfully", "filename": filename}


@app.post("/upload-garment")
async def upload_garment(file: UploadFile = File(...)):
    filename = f"garment_{uuid.uuid4().hex}{Path(file.filename).suffix}"
    file_path = GARMENTS / filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": "Garment uploaded successfully", "filename": filename}


@app.get("/list-garments")
async def list_garments():
    files = [f.name for f in GARMENTS.glob("*")]
    return files


@app.post("/try-on")
async def try_on(avatar_filename: str = Form(...), garment_filename: str = Form(...)):
    """
    Mock versiyon: avatar ve kıyafet resmini üst üste bindirip sonuç döner.
    İleride buraya AI modeli eklenecek.
    """
    avatar_path = AVATARS / avatar_filename
    garment_path = GARMENTS / garment_filename

    if not avatar_path.exists() or not garment_path.exists():
        return JSONResponse(status_code=404, content={"error": "Avatar or garment not found"})

    avatar = Image.open(avatar_path).convert("RGBA")
    garment = Image.open(garment_path).convert("RGBA")

    # Mock: kıyafeti küçültüp ortasına yapıştırıyoruz
    garment = garment.resize((int(avatar.width * 0.6), int(avatar.height * 0.6)))
    avatar.paste(garment, (int(avatar.width * 0.2), int(avatar.height * 0.2)), garment)

    result_filename = f"result_{uuid.uuid4().hex}.png"
    result_path = RESULTS / result_filename
    avatar.save(result_path)

    return {"message": "Try-on completed", "result_file": result_filename}


@app.get("/results/{filename}")
async def get_result(filename: str):
    file_path = RESULTS / filename
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"error": "Result not found"})
    return FileResponse(file_path)
