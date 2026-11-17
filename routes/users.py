from fastapi import APIRouter, HTTPException, status

from database.connection import Database
from models.users import User, UserSignIn

user_router = APIRouter(tags=["User"])
user_database = Database(User)


@user_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    if await User.find_one(User.email == user.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "User with email provided exists already.")
    await user_database.save(user)
    return {"message": "User created successfully"}


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User with email does not exist.")
    if user_exist.password == user.password:
        return {"message": "User signed in successfully."}
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid details passed.")
