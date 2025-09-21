from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from models import Base
from database import engine, get_db
import crud

# FastAPI uygulaması
app = FastAPI()

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

# Sağlık kontrol endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Avatar yükleme
@app.post("/upload-avatar/")
async def upload_avatar(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return crud.save_avatar(file, db)

# Kıyafet yükleme
@app.post("/upload-garment/")
async def upload_garment(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return crud.save_garment(file, db)

# Kıyafet deneme
@app.get("/try-on/{user_id}")
def try_on(user_id: int, db: Session = Depends(get_db)):
    return crud.try_on(user_id, db)
