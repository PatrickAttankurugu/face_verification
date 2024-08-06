from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def save_reference_image(db: Session, user_id: int, image_data: bytes):
    db_ref_image = models.ReferenceImage(user_id=user_id, image_data=image_data)
    db.add(db_ref_image)
    db.commit()
    db.refresh(db_ref_image)
    return db_ref_image

def get_reference_image(db: Session, user_id: int):
    return db.query(models.ReferenceImage).filter(models.ReferenceImage.user_id == user_id).first()