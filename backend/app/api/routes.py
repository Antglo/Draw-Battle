# backend/app/api/routes.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from app.ml.classifier import classify_image

router = APIRouter()

@router.post("/upload-drawing")
async def upload_drawing(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Read image content
    image_bytes = await file.read()

    # Process the image with the classifier
    classification = classify_image(image_bytes)
    return {"result": classification}
