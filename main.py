from fastapi import FastAPI,Depends, APIRouter
from database import get_db,init_db
from endpoints import athletes,users,performances

app = FastAPI()
#initializing the database
init_db()

#Adding the routers
app.include_router(athletes.router)

#Welcome message
@app.get("/")
def home():
    return {"message": "Welcome to the Cycling management API"}



#app.include_router(users.router,prefix="/users")    
#app.include_router(performances.router,prefix="/performances")
#pp.include_router(users.app)
#app.include_router(performances.app)#