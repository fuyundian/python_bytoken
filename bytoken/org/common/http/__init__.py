from fastapi import FastAPI

from bytoken.org.controller import UserController

app = FastAPI()

app.include_router(UserController.router, prefix="/user", tags=["user"])
