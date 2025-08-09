from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/trains",
    tags=["trains"]
)

@router.get("/", response_model=List[schemas.Train])
def read_trains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of trains."""
    trains = db.query(models.Train).offset(skip).limit(limit).all()
    return trains 