from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class TeamCreate(BaseModel):
    name:str=Field(min_length=2,max_length=150)
    short_name:str|None=Field(default=None,max_length=50)
    founded_year:int|None=Field(default=None,ge=1800,le=2100)
    api_id:int|None=None
    country_id:int|None=None
    stadium_id:int|None=None
    current_manager_id:int|None=None
class TeamRead(TeamCreate):
    model_config=ConfigDict(from_attributes=True)
    id:int
    created_at:datetime
