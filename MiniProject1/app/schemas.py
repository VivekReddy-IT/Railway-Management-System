from pydantic import BaseModel
from typing import Optional

class Train(BaseModel):
    train_id: str
    train_name: str
    train_type: str
    total_capacity: int
    frequency: str
    special_attributes: Optional[str] = None

    class Config:
        orm_mode = True 