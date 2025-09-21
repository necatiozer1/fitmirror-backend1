# FitMirror Backend (app.py)
# NOTE: Full implementation provided in canvas - simplified entry here
from fastapi import FastAPI

app = FastAPI(title="FitMirror API")

@app.get("/health")
def health():
    return {"status": "ok"}
