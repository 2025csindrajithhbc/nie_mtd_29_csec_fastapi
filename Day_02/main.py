from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/") #paths (tasks)

def home():
    return {"message" : "E-commerce Customer Support System - server"} #Seriliess

db = {
    1:{"id" : 1,"title" : "Damaged item",
       "description" : "Resolation problem",
       "category" : "Hardware",
       "status" : "New"},
    2:{"id" : 2,"title" : "Item missing",
       "description" : "refund " ,
       "category" : "empty delivity",
       "status" : "New"}
}
#schemas
class TicketCreat(BaseModel):
    title : str
    description : str
    category : str
    status : str
    
class TicketResponse(TicketCreat):
    id : int
    
#APIs
@app.get("/tickets")
def ticket_read_all():
    return list(db.values())

@app.get("/tickets/{id}")
def ticket_read_by_id(id : int):
    if id not in db:
        raise HTTPException(detail="Ticket Not found",status_code=404)
    return db[id]
@app.post("/tickets",status_code=201,response_model=TicketResponse)
def ticket_creat(ticket_payload :TicketCreat):
    new_id = max(db.keys(),default=0) + 1
    db[new_id] = {"id" : new_id, **ticket_payload.model_dump()}
    return db[new_id]

@app.put("/ticket/{id}", response_model=TicketResponse)
def tickets_update(id : int,payload : TicketCreat):
    if id not in db:
        raise HTTPException(detail="Ticket Not found" , status_code=404)
    db[id] = {"id" :id , **payload.model_dump()}
    return db[id]

@app.delete("/ticket/{id}")
def tickets_delete(id : int):
    if id not in db:
        raise HTTPException(detail="Ticket Not found",status_code=404)
    del db[id]
    return {"message" : "Ticket Deleted Successfully"}