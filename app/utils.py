import os
from fastapi import UploadFile
from deepface import DeepFace
from tempfile import NamedTemporaryFile

async def save_upload_file_temporarily(upload_file: UploadFile) -> str:
    try:
        suffix = os.path.splitext(upload_file.filename)[1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await upload_file.read()
            tmp.write(contents)
            return tmp.name
    except Exception:
        raise Exception("There was an error uploading the file")

def verify_faces(img_path1: str, img_path2: str):
    try:
        result = DeepFace.verify(img_path1, img_path2)
        return {
            "verified": result["verified"],
            "distance": result["distance"],
            "threshold": result["threshold"],
            "model": result["model"],
            "detector_backend": result["detector_backend"]
        }
    except Exception as e:
        raise Exception(f"Error during face verification: {str(e)}")