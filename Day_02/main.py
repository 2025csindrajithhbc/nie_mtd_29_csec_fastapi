from fastapi import FastAPI, HTTPException

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
@app.get("/tickets")
def ticket_read_all():
    return list(db.values())

@app.get("/tickets/{id}")
def ticket_read_by_id(id : int):
    return db[id]