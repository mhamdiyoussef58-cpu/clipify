from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, uuid, subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"status": "ok", "service": "clipify-backend"}

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.mp4', '.mov', '.webm')):
        raise HTTPException(400, "Supported: mp4, mov, webm")
    
    uid = uuid.uuid4().hex
    file_path = os.path.join(UPLOAD_DIR, f"{uid}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return JSONResponse({
        "success": True,
        "file_path": file_path,
        "message": "تم استلام الفيديو - المعالجة قيد التطوير"
    })

@app.get("/health")
def health():
    return {"ok": True}
