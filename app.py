import os
import replicate
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# env.txt dosyasını yükle
load_dotenv("env.txt")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== AI Try-On Endpoint ==========
@app.post("/try-on")
async def try_on(avatar: UploadFile = File(...), garment: UploadFile = File(...)):
    # Klasörler oluştur
    os.makedirs("avatars", exist_ok=True)
    os.makedirs("garments", exist_ok=True)

    # Dosya yolları
    avatar_path = f"avatars/{uuid.uuid4()}_{avatar.filename}"
    garment_path = f"garments/{uuid.uuid4()}_{garment.filename}"

    # Dosyaları kaydet
    with open(avatar_path, "wb") as f:
        f.write(await avatar.read())
    with open(garment_path, "wb") as f:
        f.write(await garment.read())

    # Replicate modelini çağır
    output = replicate.run(
        "yisol/tryondiffusion:db21e61269a6d9a74c72114d8351fbd882f7b151c9a2cf47d6f5c01b21ccf8b9",
        input={
            "person_img": open(avatar_path, "rb"),
            "garment_img": open(garment_path, "rb")
        }
    )

    # Çıktıyı döndür
    return {"result": output}
