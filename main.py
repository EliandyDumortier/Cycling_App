from fastapi import FastAPI,Depends, APIRouter
from database import get_db,init_db
from endpoints import athletes,users,performances,stats

app = FastAPI()
#initializing the database
init_db()

#Adding the routers
app.include_router(athletes.app)
app.include_router(users.app)
app.include_router(performances.app)
app.include_router(stats.app)

#Welcome message
@app.get("/")
def home():
    return {"message": "Welcome to the Cycling management API"}
