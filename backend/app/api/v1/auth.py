from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register(payload: RegisterRequest):
    return {"message": "User registered", "email": payload.email}


@router.post("/login")
def login(payload: LoginRequest):
    return {"access_token": create_access_token(subject=payload.email), "token_type": "bearer"}


@router.post("/refresh")
def refresh():
    return {"message": "Refresh token endpoint"}


@router.get("/me")
def me():
    return {"role": "student"}
