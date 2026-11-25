from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

# Create a FastAPI instance
app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    "image/jpeg", 
    "image/png", 
    "image/webp"
    }

@app.post("/upload/")
async def upload_Image(image: UploadFile = File(...)):
    
    if image.content_type not in ALLOWED_EXTENSIONS:
        return {"error": "Invalid file type. Only JPEG, PNG, and WEBP images are allowed."}

    unique_id = uuid.uuid4().hex
    extension = ALLOWED_EXTENSIONS[image.content_type]

    filename = f"{unique_id}{extension}"
    file_path = UPLOAD_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

        return{
            "message": f"Image '{image.filename}' uploaded successfully.",
            "filename": image.filename,
            "saved_to": str(file_path)
        }

@app.get("/media")
async def get_media():
    media = []

    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file():
            media.append({
                "filename": file_path.name,
                "path": str(file_path)
            })
    return {"media": media}

    # Reusable function to find an image
def find_media_file(media_id: str):
    for extension in ALLOWED_EXTENSIONS.values():
        candidate = UPLOAD_DIR / f"{media_id}{extension}"

        if candidate.is_file():
            return candidate

    return None

@app.post("/project/{media_id}")
async def project_image(media_id: str):
      # Assuming the images are saved with .png extension
    image_path = UPLOAD_DIR / f"{media_id}.png"

    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found.")

    return{
        "message": "Image Found!",
        "media_id": media_id,
        "image_path": str(image_path)
    }