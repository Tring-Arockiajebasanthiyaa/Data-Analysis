from fastapi import FastAPI , HTTPException , status
from pydantic import BaseModel , ValidationError
from typing import List

app = FastAPI()

class Item(BaseModel):
    id:int
    name:str
    price:int

items=[]
@app.get("/items",response_model=List[Item])
async def get_items():
    return items
    
        
@app.post("/items/create_item",response_model=Item)
async def create_items(item:Item):
    items.append(item)
    return item
        
   

@app.put("/items/update/{item_id}",response_model=Item)
async def update_items(item_id:int,item:Item):
     items[item_id]=item
     return item
       
    

@app.delete("/items/{item_id}")
async def delete_items(item_id:int):
    del items[item_id]
    return {"message":"items deleted successfully"}



        
    
