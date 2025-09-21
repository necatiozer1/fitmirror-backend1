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
from . import models, database, crud

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

STORAGE = Path(os.getenv("STORAGE_DIR", "./storage")).resolve()
AVATARS = STORAGE / "avatars"
GARMENTS = STORAGE / "garments"
RESULTS = STORAGE / "results"
for p in (AVATARS, GARMENTS, RESULTS):
    p.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="FitMirror API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
# Kullanıcı uçları (DB ile)
############################################
class UserResp(BaseModel):
    uid: str
    email: str | None
    is_subscriber: bool
    has_used_free_hq: bool

    class Config:
        orm_mode = True

@app.post("/user/upsert", response_model=UserResp)
def upsert_user(uid: str, email: str | None = None, db: Session = Depends(get_db)):
    return crud.upsert_user(db, uid, email)

@app.get("/user/{uid}", response_model=UserResp)
def get_user(uid: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, uid)
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)
    return user

@app.post("/user/consume_free_hq", response_model=UserResp)
def consume_free_hq(uid: str, db: Session = Depends(get_db)):
    user = crud.consume_free_hq(db, uid)
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)
    return user

@app.post("/user/set_subscriber", response_model=UserResp)
def set_subscriber(uid: str, is_subscriber: bool, db: Session = Depends(get_db)):
    user = crud.set_subscriber(db, uid, is_subscriber)
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)
    return user

############################################
# Upload uçları
############################################
class UploadResp(BaseModel):
    url: str
    id: str

@app.post("/upload/avatar", response_model=UploadResp)
async def upload_avatar(uid: str = Form(...), file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower() or ".jpg"
    avatar_id = f"{uid}_{uuid.uuid4()}" + ext
    dest = AVATARS / avatar_id
    with open(dest, "wb") as f:
        f.write(await file.read())
    return UploadResp(url=f"/files/avatars/{avatar_id}", id=avatar_id)

@app.post("/upload/garment", response_model=UploadResp)
async def upload_garment(uid: str = Form(...), file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower() or ".png"
    garment_id = f"{uid}_{uuid.uuid4()}" + ext
    dest = GARMENTS / garment_id
    with open(dest, "wb") as f:
        f.write(await file.read())
    return UploadResp(url=f"/files/garments/{garment_id}", id=garment_id)

@app.get("/files/{folder}/{name}")
def get_file(folder: str, name: str):
    path = STORAGE / folder / name
    if not path.exists():
        return JSONResponse({"error": "not found"}, status_code=404)
    return FileResponse(path)

############################################
# Avatar ve Try-On uçları
############################################
class JobResp(BaseModel):
    job_id: str
    status: str
    result_url: Optional[str] = None

@app.post("/avatar/build", response_model=JobResp)
def build_avatar(uid: str, avatar_id: str):
    src = AVATARS / avatar_id
    if not src.exists():
        return JSONResponse({"error": "avatar not found"}, status_code=404)
    img = Image.open(src).convert("RGBA")
    img.thumbnail((1024, 1024))
    out_name = f"{uid}_avatar_preview.png"
    out_path = RESULTS / out_name
    img.save(out_path)
    return JobResp(job_id=str(uuid.uuid4()), status="done", result_url=f"/files/results/{out_name}")

@app.post("/tryon/fast", response_model=JobResp)
def tryon_fast(uid: str, avatar_result_name: str, garment_id: str):
    avatar = Image.open(RESULTS / avatar_result_name).convert("RGBA")
    garment = Image.open(GARMENTS / garment_id).convert("RGBA")
    garment.thumbnail((int(avatar.width*0.6), int(avatar.height*0.6)))
    composed = avatar.copy()
    composed.alpha_composite(garment, (avatar.width//4, avatar.height//3))
    out_name = f"{uid}_tryon_fast.png"
    out_path = RESULTS / out_name
    composed.save(out_path)
    return JobResp(job_id=str(uuid.uuid4()), status="done", result_url=f"/files/results/{out_name}")

@app.post("/tryon/hq", response_model=JobResp)
def tryon_hq(uid: str, avatar_result_name: str, garment_id: str):
    avatar = Image.open(RESULTS / avatar_result_name).convert("RGBA")
    garment = Image.open(GARMENTS / garment_id).convert("RGBA")
    garment = garment.resize((avatar.width//2, avatar.height//2))
    composed = avatar.copy()
    composed.alpha_composite(garment, (avatar.width//3, avatar.height//3))
    out_name = f"{uid}_tryon_hq.png"
    composed.save(RESULTS / out_name)
    return JobResp(job_id=str(uuid.uuid4()), status="done", result_url=f"/files/results/{out_name}")
