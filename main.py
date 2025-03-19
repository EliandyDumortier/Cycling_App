from fastapi import FastAPI
from endpoints.users import router as user_router

app = FastAPI()
app.include_router(user_router)
