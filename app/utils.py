import cv2
import numpy as np
from deepface import DeepFace
from fastapi import UploadFile
from tempfile import NamedTemporaryFile
import os

async def save_upload_file_temporarily(upload_file: UploadFile) -> str:
    try:
        suffix = os.path.splitext(upload_file.filename)[1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await upload_file.read()
            tmp.write(contents)
            return tmp.name
    except Exception:
        raise Exception("There was an error uploading the file")

def verify_faces(img1_path: str, img2_path: str):
    try:
        result = DeepFace.verify(img1_path, img2_path)
        return {
            "verified": result["verified"],
            "distance": result["distance"],
            "threshold": result["threshold"],
            "model": result["model"],
            "detector_backend": result["detector_backend"]
        }
    except Exception as e:
        raise Exception(f"Error during face verification: {str(e)}")

def image_to_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as image_file:
        return image_file.read()

def bytes_to_image(image_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)