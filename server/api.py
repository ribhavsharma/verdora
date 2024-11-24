from fastapi import FastAPI, Body # type: ignore
from typing import Union
from mysql_manager import MysqlManager
from pydantic import BaseModel
import hashlib
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()

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
    
class ItemDetailsRequest(BaseModel):
    itemId: int

@app.post("/signUp")
def sign_up(request: SignupRequest):
    mysql = MysqlManager()
    hashed_password = hashlib.md5(request.password.encode()).hexdigest()
    mysql.insert_data(
        "users",
        {"username": request.username, "password": hashed_password}
    )
    mysql.close_connection()
    return {"message": "User signed up successfully", "username": request.username}

@app.post("/signIn")
def sign_in(request: SignupRequest):
    mysql = MysqlManager()
    hashed_password = hashlib.md5(request.password.encode()).hexdigest()
    signInDb = mysql.select_data(
        "users",
        "password",
        where_clause=f"username = '{request.username}' AND password = '{hashed_password}'"
    )
    mysql.close_connection()
    return {1 if signInDb else 0}

@app.post("/userDetails")
def get_user_details(request: UserDetailsRequest):

    mysql = MysqlManager()
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
    mysql.close_connection()
    return {
        "name": user_detail[0],
        "email": user_detail[1],
        "phone_number": user_detail[2],
        "listings": listings
        
    }
    
@app.post("/updateUser")
def update_user(request: UserUpdateRequest):

    mysql = MysqlManager()
    mysql.update_data(
        "users",
        {"email": request.email, "phone_number": request.phone_number},
        f"username = '{request.username}'"
    )
    mysql.close_connection()
    return {"message": "User details updated successfully"}

@app.post("/image")
def image(request: ImageRequest):
    data = request.data 
    return {"message": "Image received successfully", "data_echo": data}

@app.post("/sellItem")
def sell_item(request: dict):

    mysql = MysqlManager()
    mysql.insert_data(
        "items_for_sale",
        {
            "category": request["item_name"],
            "user_name": request["username"],
        }
    )
        
    mysql.close_connection()
    return {"message": "Item added successfully"}

@app.post("/getItemDetails")
def get_item_details(request: ItemDetailsRequest):
    item_id = request.itemId
    if not item_id:
        return {"message": "Item ID is required"}
    
    mysql = MysqlManager()
    
     # Fetch item details
    item_details = mysql.select_data(
        "items_for_sale",
        "category, price, user_name",
        where_clause=f"id = {item_id}"
    )

    if not item_details:
        mysql.close_connection()
        return {"message": "Item not found"}

    item_detail = item_details[0]
    category = item_detail[0]
    price = item_detail[1]
    user_name = item_detail[2]

    # Fetch user details
    user_details = mysql.select_data(
        "users",
        "email, phone_number",
        where_clause=f"username = '{user_name}'"
    )

    if not user_details:
        mysql.close_connection()
        return {"message": "User details not found for this item"}

    user_detail = user_details[0]
    email = user_detail[0]
    phone_number = user_detail[1]

    mysql.close_connection()

    return {
        "category": category,
        "price": str(price),
        "seller_contact": {
            "username": user_name,
            "email": email,
            "phone_number": phone_number,
        },
    }
