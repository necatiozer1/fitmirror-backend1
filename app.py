from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base
import crud

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    filename = file.filename
    # DB işlemi örnek
    crud.create_file(db=db, filename=filename, content=content)
    return {"filename": filename, "size": len(content)}
