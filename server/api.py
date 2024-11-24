from fastapi import FastAPI, Body # type: ignore
from typing import Union
from mysql_manager import MysqlManager
from pydantic import BaseModel
import hashlib
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()
mysql = MysqlManager()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins like ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageRequest(BaseModel):
    data: str  # Expect the `data` field as a string

class SignupRequest(BaseModel):
    username: str
    password: str

class UserDetailsRequest(BaseModel):
    username: str

class UserUpdateRequest(BaseModel):
    username: str
    email: str
    phone_number: str

@app.post("/signUp")
def sign_up(request: SignupRequest):
    hashed_password = hashlib.md5(request.password.encode()).hexdigest()
    mysql.insert_data(
        "users",
        {"username": request.username, "password": hashed_password}
    )
    return {"message": "User signed up successfully", "username": request.username}

@app.post("/signIn")
def sign_in(request: SignupRequest):
    hashed_password = hashlib.md5(request.password.encode()).hexdigest()
    signInDb = mysql.select_data(
        "users",
        "password",
        where_clause=f"username = '{request.username}' AND password = '{hashed_password}'"
    )
    return {1 if signInDb else 0}

@app.post("/userDetails")
def get_user_details(request: UserDetailsRequest):
    user_details = mysql.select_data(
        "users",
        "username, email, phone_number",
        where_clause=f"username = '{request.username}'"
    )
    if not user_details:
        return {"message": "User not found"}
    user_detail = user_details[0]
    
    user_listings = mysql.select_data(
        "items_for_sale",
        "category",
        where_clause=f"user_name = '{request.username}'"
    )
    
    # Format the listings
    listings = [{"category": listing[0]} for listing in user_listings]
    
    return {
        "name": user_detail[0],
        "email": user_detail[1],
        "phone_number": user_detail[2],
        "listings": listings
        
    }
    
@app.post("/updateUser")
def update_user(request: UserUpdateRequest):
    mysql.update_data(
        "users",
        {"email": request.email, "phone_number": request.phone_number},
        f"username = '{request.username}'"
    )
    return {"message": "User details updated successfully"}

@app.post("/image")
def image(request: ImageRequest):
    data = request.data 
    return {"message": "Image received successfully", "data_echo": data}

@app.post("/sellItem")
def sell_item(request: dict):
    mysql.insert_data(
        "items_for_sale",
        {
            "category": request["item_name"],
            "user_name": request["username"],
        }
    )
        
    
    return {"message": "Item added successfully"}
