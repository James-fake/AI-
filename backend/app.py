from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import subprocess
import zipfile
from pathlib import Path

app = FastAPI(title="AI Animal Sticker Generator")

UPLOAD_DIR = Path("uploads")
EXPORT_DIR = Path("exports")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/generate")
async def generate_stickers(
    animal_photo: UploadFile = File(...),
    style: str = "cartoon",
    emoji_type: str = "开心"
):
    temp_path = UPLOAD_DIR / f"{uuid.uuid4()}.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(animal_photo.file, buffer)
    
    try:
        result = subprocess.run(
            ["python", "scripts/run_comfy.py", str(temp_path), style, emoji_type],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        
        zip_path = EXPORT_DIR / f"{uuid.uuid4()}.zip"
        with zipfile.ZipFile(zip_path, 'w') as z:
            for i in range(9):
                img_path = OUTPUT_DIR / f"sticker_{i+1}.webp"
                if img_path.exists():
                    z.write(img_path, f"sticker_{i+1}.webp")
        
        return FileResponse(str(zip_path), media_type="application/zip", filename=zip_path.name)
    
    finally:
        if temp_path.exists():
            temp_path.unlink()
