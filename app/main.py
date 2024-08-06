from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from .utils import save_upload_file_temporarily, verify_faces
from .camera import capture_image
import os

app = FastAPI()

reference_image = None

@app.post("/upload_reference/")
async def upload_reference(file: UploadFile = File(...)):
    global reference_image
    try:
        reference_image = await save_upload_file_temporarily(file)
        return {"message": "Reference image uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify/")
async def verify_face():
    global reference_image
    if not reference_image:
        raise HTTPException(status_code=400, detail="Reference image not uploaded")
    
    try:
        live_image = capture_image()
        result = verify_faces(reference_image, live_image)
        
        # Clean up live image
        os.remove(live_image)
        
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Face Verification API"}