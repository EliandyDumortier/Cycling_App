from fastapi import FastAPI, APIRouter
from endpoints import athletes,users,performances,stats

app = FastAPI()

#Adding the routers
app.include_router(users.router)
app.include_router(athletes.router)
app.include_router(performances.router)
app.include_router(stats.router)

#Welcome message
@app.get("/")
def home():
    return {"message": "Welcome to the Cycling management API"}
