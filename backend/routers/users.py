from fastapi import APIRouter, HTTPException, HTTPException
from pydantic import BaseModel

from backend.managers.auth_manager import create_user, login_user

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/login")
def login(login_request: LoginRequest):
    # Check if the user exists and the credentials are valid
    if login_user(login_request.username, login_request.password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/register")
def register(register_request: RegisterRequest):
    # Check if the user already exists
    if login_user (register_request.username, register_request.password):
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        # Create the user
        create_user(
            firstname=register_request.firstname,
            lastname=register_request.lastname,
            username=register_request.username,
            password=register_request.password
        )
        return {"message": "User created successfully"}
