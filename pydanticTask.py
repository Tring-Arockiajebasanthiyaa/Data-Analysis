from pydantic import BaseModel , ValidationError
from datetime import datetime
from typing import Optional

class Address(BaseModel):
    street:str
    door_no:int
    place:str
    
class User(BaseModel):
    name:str
    age:int
    address:Optional[Address] = None
    createdAt: datetime = datetime.now()


data={
    "name":"Sandy",
    "age":21,
    "address":{
        "street":"West Street",
        "door_no":8,
        "place":"Tirunelveli"
        }
}

user=User(**data)
print(user)
