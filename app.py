import os
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from PIL import Image

app = FastAPI()

# CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Klasörler
STORAGE = Path("./storage").resolve()
AVATARS = STORAGE / "avatars"
GARMENTS = STORAGE / "garments"
RESULTS = STORAGE / "results"
for folder in [STORAGE, AVATARS, GARMENTS, RESULTS]:
    folder.mkdir(parents=True, exist_ok=True)

# Sağlık testi
@app.get("/health")
def health():
    return {"status": "ok"}

# Avatar yükle
@app.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...)):
    filename = f"avatar_{uuid.uuid4().hex}.jpg"
    filepath = AVATARS / filename
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": "Avatar uploaded successfully", "filename": filename}

# Kıyafet yükle
@app.post("/upload-garment")
async def upload_garment(file: UploadFile = File(...)):
    filename = f"garment_{uuid.uuid4().hex}.jpg"
    filepath = GARMENTS / filename
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": "Garment uploaded successfully", "filename": filename}

# Kıyafetleri listele
@app.get("/list-garments")
def list_garments():
    garments = [f.name for f in GARMENTS.glob("*.jpg")]
    return garments

# Avatar + kıyafeti birleştir
@app.post("/try-on")
async def try_on():
    try:
        avatar_files = list(AVATARS.glob("*.jpg"))
        garment_files = list(GARMENTS.glob("*.jpg"))

        if not avatar_files or not garment_files:
            return {"error": "Avatar veya kıyafet bulunamadı"}

        avatar_path = avatar_files[-1]  # son yüklenen avatar
        garment_path = garment_files[-1]  # son yüklenen kıyafet

        avatar = Image.open(avatar_path).convert("RGBA")
        garment = Image.open(garment_path).convert("RGBA")

        # Kıyafeti boyutlandır ve avatarın üzerine koy
        garment = garment.resize((avatar.width, int(avatar.height / 2)))
        avatar.paste(garment, (0, avatar.height // 2), garment)

        result_filename = f"result_{uuid.uuid4().hex}.png"
        result_path = RESULTS / result_filename
        avatar.save(result_path)

        return {"message": "Try-on başarılı", "filename": result_filename}
    except Exception as e:
        return {"error": str(e)}

# Sonuç dosyalarını göster
@app.get("/results/{filename}")
async def get_result(filename: str):
    filepath = RESULTS / filename
    if filepath.exists():
        return FileResponse(filepath)
    return {"error": "Dosya bulunamadı"}
