from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class CountryCreate(BaseModel):
    name: str=Field(min_length=2,max_length=100)
    code: str|None=Field(default=None,max_length=10)
class CountryRead(CountryCreate):
    model_config=ConfigDict(from_attributes=True)
    id:int
    created_at:datetime
