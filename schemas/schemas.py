
from pydantic import BaseModel, constr, conint, validator, conlist
from typing import Optional
from datetime import datetime

class BaseAudio(BaseModel):
    id:int
    duration: conint(ge=0)
    uploadTime: datetime

    @validator("uploadTime")
    def parse_birthdate(cls, value):
        value = datetime.now()
        return value

class Song(BaseAudio):
    name: constr(max_length=100)

class Podcast(BaseAudio):
    name: constr(max_length=100)
    host: constr(max_length=100)
    participants : Optional[conlist(constr(max_length=100), min_items=1, max_items=10)]

class Audiobook(BaseAudio):
    title:constr(max_length=100)
    author:constr(max_length=100)
    narrator:constr(max_length=100)

    