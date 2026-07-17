from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
import shutil

app = FastAPI()

# -----------------------------
# Base Directories
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
CLIENT_DIR = BASE_DIR / "client"
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "uploads"

# Create uploads folder if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)

print("Current Working Directory:", os.getcwd())
print("BASE_DIR:", BASE_DIR)
print("CLIENT_DIR Exists:", CLIENT_DIR.exists())
print("STATIC_DIR Exists:", STATIC_DIR.exists())

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Static Files
# -----------------------------
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# -----------------------------
# Home Page
# -----------------------------
@app.get("/")
async def home():
    index_file = CLIENT_DIR / "index.html"

    if index_file.exists():
        return FileResponse(str(index_file))

    raise HTTPException(status_code=404, detail="index.html not found")

# -----------------------------
# HTML Pages
# -----------------------------
@app.get("/{page_name}")
async def get_page(page_name: str):

    file_path = CLIENT_DIR / page_name

    if file_path.exists():
        return FileResponse(str(file_path))

    html_file = CLIENT_DIR / f"{page_name}.html"

    if html_file.exists():
        return FileResponse(str(html_file))

    raise HTTPException(status_code=404, detail="Page not found")

# -----------------------------
# Upload Audio
# -----------------------------
@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    try:
        save_path = UPLOAD_DIR / file.filename

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "filename": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Process Meeting
# -----------------------------
@app.post("/process-meeting/{filename}")
async def process_meeting(filename: str):

    return {
        "message": f"Processing {filename}..."
    }

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
async def health():
    return {
        "status": "running"
    }