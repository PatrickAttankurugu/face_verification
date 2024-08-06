from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth
from .database import engine, get_db
from .utils import save_upload_file_temporarily, verify_faces, image_to_bytes, bytes_to_image
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload_reference/")
async def upload_reference(file: UploadFile = File(...), current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    temp_file = await save_upload_file_temporarily(file)
    image_data = image_to_bytes(temp_file)
    crud.save_reference_image(db, current_user.id, image_data)
    os.remove(temp_file)
    return {"message": "Reference image uploaded successfully"}

@app.post("/verify/", response_model=schemas.VerificationResult)
async def verify_face(file: UploadFile = File(...), current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    reference_image = crud.get_reference_image(db, current_user.id)
    if not reference_image:
        raise HTTPException(status_code=400, detail="Reference image not found")
    
    temp_file = await save_upload_file_temporarily(file)
    
    with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_ref:
        tmp_ref.write(reference_image.image_data)
        tmp_ref_name = tmp_ref.name
    
    try:
        result = verify_faces(tmp_ref_name, temp_file)
        return result
    finally:
        os.remove(temp_file)
        os.remove(tmp_ref_name)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Face Verification API"}