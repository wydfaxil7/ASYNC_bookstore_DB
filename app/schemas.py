from pydantic import BaseModel

class BookBase(BaseModel):
    name: str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}  # replaces orm_mode