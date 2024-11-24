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
    mysql.insert_data(
        "items_for_sale",
        {
            "category": request["item_name"],
            "user_name": request["username"],
            "image": request["image"],
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
        "category, price, user_name, image",
        where_clause=f"id = {item_id}"
    )

    if not item_details:
        mysql.close_connection()
        return {"message": "Item not found"}

    item_detail = item_details[0]
    category = item_detail[0]
    price = item_detail[1]
    user_name = item_detail[2]
    image = item_detail[3]

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
        "image": image, 
        "seller_contact": {
            "username": user_name,
            "email": email,
            "phone_number": phone_number,
        },
    }

@app.get("/getAllItems")
def get_all_item_details():
    mysql = MysqlManager()
    items = mysql.select_data("items_for_sale", "id, category, price, image", where_clause="sold = 0")
    mysql.close_connection()
    return [{"id": item[0], "name": item[1], "price": str(item[2]), "image": item[3]} for item in items]

@app.post("/markAsSold")
def mark_as_sold(request: ItemDetailsRequest):
    mysql = MysqlManager()
    mysql.update_data(
        "items_for_sale",
        {"sold": 1},
        where_clause=f"id = {request.itemId}"
    )
    mysql.close_connection()
    return {"message": "Item marked as sold"}