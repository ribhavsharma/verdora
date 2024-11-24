from fastapi import FastAPI, Body # type: ignore
from typing import List, Union
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
    wishlist: List[str]

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

    # get wishlist items
    wishlist = mysql.select_data(
        "wishlist",
        "item",
        where_clause=f"userId = '{user_detail[0]}'"
    )
    wishlist = [i[0] for i in wishlist]
    print(user_detail)
    mysql.close_connection()
    return {
        "name": user_detail[1],
        "email": user_detail[3],
        "phone_number": user_detail[4],
        "listings": listings,
        "wishlist": wishlist
    }
    
@app.post("/updateUser")
def update_user(request: UserUpdateRequest):

    mysql = MysqlManager()
    mysql.update_data(
        "users",
        {"email": request.email, "phone_number": request.phone_number},
        f"username = '{request.username}'"
    )

    userId = mysql.get_user_id(request.username)[0][0]

    wishlistItems = request.wishlist
    # check if wishlist item already exists in users database
    existingItems = mysql.select_data(
            "wishlist",
            "*",
            where_clause=f"userId = '{userId}'"
        )
    
    existingItems = [item[2] for item in existingItems]

    for item in wishlistItems:
        if item in existingItems: 
            existingItems.remove(item)
            continue

        mysql.insert_data("wishlist",
                          {
                              'userId': userId,
                              'item': item
                          })

    for leftOutItems in existingItems:
        mysql.delete_data("wishlist", where_clause=f"userid={userId} AND item='{leftOutItems}'")

    mysql.close_connection()
    return {"message": "User details updated successfully"}

@app.post("/image")
def image(request: ImageRequest):
    data = request.data 
    return {"message": "Image received successfully", "data_echo": data}

@app.post("/sellItem")
def sell_item(request: dict):

    mysql = MysqlManager()
    itemId = mysql.insert_data(
        "items_for_sale",
        {
            "category": request["item_name"],
            "user_name": request["username"],
        }
    )

    userId = mysql.get_user_id(request["username"])[0][0]
    item = request["item_name"]
    # check users who want this item
    usersWhoHaveItemInWishlist = mysql.select_data(
        "wishlist",
        where_clause=f"userId != '{userId}' AND item='{item}'"
    )

    for user in usersWhoHaveItemInWishlist:
        buyerId = user[1]
        mysql.insert_data(
            "notifications",
            {
                "userId": buyerId,
                "itemId": itemId,
            }
        )

    mysql.close_connection()
    return {"message": "Item added successfully"}
