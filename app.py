import os
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

# Storage klasörü
STORAGE = Path("./storage")
AVATARS = STORAGE / "avatars"
AVATARS.mkdir(parents=True, exist_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...)):
    try:
        # Benzersiz dosya adı üretelim
        ext = os.path.splitext(file.filename)[-1]
        filename = f"{uuid.uuid4()}{ext}"
        filepath = AVATARS / filename

        # Dosyayı kaydet
        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())

        return {"status": "success", "filename": filename}

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
