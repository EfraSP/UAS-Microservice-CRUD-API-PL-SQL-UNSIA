from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from crud import create_user, get_user, update_user_password, delete_user

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

@app.post("/create_user/")
def create_user_endpoint(user: User):
    create_user(user.username, user.password)
    return {"message": "User created successfully"}

@app.get("/get_user/")
def get_user_endpoint(username: str):
    user = get_user(username)
    if user:
        return {"username": user[0], "password": user[1]}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/update_password/")
def update_password_endpoint(username: str, new_password: str):
    update_user_password(username, new_password)
    return {"message": "Password updated successfully"}

@app.delete("/delete_user/")
def delete_user_endpoint(username: str):
    delete_user(username)
    return {"message": "User deleted successfully"}
