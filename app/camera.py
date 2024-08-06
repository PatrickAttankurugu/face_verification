import cv2
import os
from tempfile import NamedTemporaryFile

def capture_image():
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera
    
    if not cap.isOpened():
        raise Exception("Could not open camera")
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise Exception("Could not capture image")
    
    with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        cv2.imwrite(tmp.name, frame)
        return tmp.name