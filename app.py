import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from PIL import Image

from sqlalchemy.orm import Session
from models import Base
from database import engine, SessionLocal
import crud

# -------------------- Uygulama --------------------
app = FastAPI()

# CORS ayarı (gerekirse frontend erişsin diye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Health Check --------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------- Veritabanı --------------------
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- Örnek Endpoint --------------------
class Item(BaseModel):
    name: str
    description: Optional[str] = None

@app.post("/items/")
def create_item(item: Item, db: Session = Depends(get_db)):
    # Burada crud fonksiyonlarını kullanabilirsin
    return {"name": item.name, "description": item.description}

# -------------------- Dosya Yükleme Örneği --------------------
STORAGE = Path(os.getenv("STORAGE_DIR", "./storage")).resolve()
AVATARS = STORAGE / "avatars"
RESULTS = STORAGE / "results"

# klasörleri oluştur
for folder in [STORAGE, AVATARS, RESULTS]:
    folder.mkdir(parents=True, exist_ok=True)

@app.post("/upload-avatar/")
async def upload_avatar(file: UploadFile = File(...)):
    file_path = AVATARS / f"{uuid.uuid4()}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": str(file_path)}
