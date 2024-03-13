from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    last_name: str
    phone_number: str
    age: int
    creation_time: datetime = datetime.now()


class UserRequest(BaseModel):
    name: str
    last_name: str
    phone_number: str
    age: int
