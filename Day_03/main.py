from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

import jwt
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone

# app
app = FastAPI()

#db config
URL = "mongodb://127.0.0.1:27017"
client = MongoClient(URL)
db = client["Support_ticket_db"]
ticket_collection = db["tickets"]
user_collection = db["users"]

#security config
password_hash = PasswordHash.recommended()
SECRET_KEY= 

# pydantic schama

class TicketCreate(BaseModel):
    title : str
    description : str
    catagory : str
    status : str

class TicketResponse(TicketCreate):
    id : str

#....users
class UserCreate(BaseModel):
    username : str
    password : str
    role : int
    
#....token
class TokenResponse(BaseModel):
    access_token : str
    token_type : str

# helper
def ticket_helper(ticket_doc):
    return {
        "id" : str(ticket_doc["_id"]),
        "title" : ticket_doc["title"],
        "description" : ticket_doc["description"],
        "catagory" : ticket_doc["catagory"],
        "status" : ticket_doc["status"]
    } 
#....user_helper
def user_helper(user):
    return{
        "id" : str(user["_id"]),
        "username" : user["username"],
        "role" : user["role"]
    }
    
# create jwt
def create_token(username : str,role : int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINS)
#apis - CRUD ,read all, read by id , update ,delete
@app.post("/tickets",status_code=201,response_model=TicketResponse)
def ticket_create(payload : TicketCreate):
    ticket_dict = payload.model_dump()
    result = ticket_collection.insert_one(ticket_dict)
    new_ticket = ticket_collection.find_one({"_id" : result.inserted_id})
    return ticket_helper(new_ticket)

@app.get("/tickets",response_model=list[TicketResponse])
def ticket_read_all():
    docs = ticket_collection.find()
    tickets = [ticket_helper(doc) for doc in docs]
    return tickets

@app.get("/tickets/{id}",response_model=TicketResponse)
def ticket_read_by_id(id : str):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid Ticket ID",status_code=403)
    doc = ticket_collection.find_one({"_id" : ObjectId(id)})
    if not doc:
        raise HTTPException(detail= "Ticket NOt found" ,status_code=404)
    return ticket_helper(doc)

@app.put("/tickets/{id}",response_model=TicketResponse)
def ticket_update(id : str , payload:TicketCreate):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid Ticket ID",status_code=403)
    ticket_dict = payload.model_dump()
    result = ticket_collection.update_many({"_id" : ObjectId(id)},
                                          {"$set" : ticket_dict})
    if result.matched_count == 0:
        raise HTTPException(detail="Ticket Not Found", status_code=404)
    new_ticket = ticket_collection.find_one({"_id" : ObjectId(id)})
    return ticket_helper(new_ticket)
    
@app.delete("/tickets/{id}")
def ticket_delete(id:str):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid Ticket ID",status_code=403)
    result = ticket_collection.delete_one({"_id" : ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(detail="Ticket Not Found", status_code=404)
    return {"message" : "Ticket Deleted Succcessfuly"}