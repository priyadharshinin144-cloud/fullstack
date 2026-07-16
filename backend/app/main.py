from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI()

# 1. CORS Setup: Allows your frontend (running on localhost) to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Static Files: Mounts folders to serve images and styles
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Routes for your HTML pages
@app.get("/")
async def read_index():
    return FileResponse('client/<a href="second.html">')

@app.get("/{page_name}")
async def get_page(page_name: str):
    # This checks if the file exists in your client folder
    file_path = f"client/{page_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    # If the user typed "second" instead of "second.html", handle that:
    elif os.path.exists(f"client/{page_name}.html"):
        return FileResponse(f"client/{page_name}.html")
    raise HTTPException(status_code=404, detail="Page not found")
# 4. API Endpoint: To handle audio file uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    """Saves the audio file uploaded from your frontend."""
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. Placeholder for AI Processing
@app.post("/process-meeting/{filename}")
async def process_meeting(filename: str):
    """Trigger this after the file is uploaded to run transcription."""
    return {"message": f"Processing {filename} logic will go here."}