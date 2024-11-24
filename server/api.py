from typing import Union
from mysql_manager import MysqlManager
from fastapi import FastAPI # type: ignore
from pydantic import BaseModel
import hashlib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
mysql =MysqlManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins like ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SignupRequest(BaseModel):
    username: str
    password: str


@app.post("/signUp")
def signUp(request: SignupRequest):

    hashed_password = hashlib.md5(request.password.encode()).hexdigest()

    mysql.insert_data(
        "users",
        {"username": request.username,"password": hashed_password}
    )
    return {"message": "User signed up successfully", "username": request.username}

@app.post("/signIn")
def signUp(request: SignupRequest):

    hashed_password = hashlib.md5(request.password.encode()).hexdigest()

    signInDb = mysql.select_data(
        "users",
        "password",
        where_clause=f"username = '{request.username}' AND password = '{hashed_password}'"
    )

    return len(signInDb)