from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends, APIRouter
from typing import Annotated
from Core.db import get_session
from Schema.userschema import UserCreate, UserPublic
from Model.Models import User
from crud import CrudUser
from Core.auth import get_current_user, create_access_token,is_admin
from Core.security import verify_password
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(
    user: UserCreate, session: Annotated[AsyncSession, Depends(get_session)],*,current_user:Annotated[User,Depends(is_admin())]
) -> User:
    user = await CrudUser.create_user(user=user, session=session)
    return user


@router.get("/by_id/{userid}", response_model=UserPublic)
async def get_user_by_id(
    userid: int, session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await CrudUser.get_user_by_id(user_id=userid, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/by_name/{username}", response_model=UserPublic)
async def get_user_by_name(
    username: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await CrudUser.get_user_by_name(username=username, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/my_session", response_model=UserPublic)
async def read_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/token", response_model=dict)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    user = await CrudUser.get_user_by_name(username=form_data.username, session=session)
    if not user or not verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authentication": "Bearer"},
        )
    access_token = create_access_token(data={"sub":user.username})
    return {"access_token":access_token,"token_type":"bearer"}