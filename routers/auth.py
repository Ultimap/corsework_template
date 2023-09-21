from fastapi import APIRouter, Depends, HTTPException, Form
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from models import Users
from database import get_session, get_user_by_username, get_user_by_jwt
from datetime import datetime, timedelta
import jwt
from settings import SECRET_KEY, ALGORITH
from sqlalchemy import update
from typing import Optional

EXPIRATION_TIME = timedelta(minutes=30)

auth = APIRouter(prefix='/auth', tags=['User'])


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str


async def hashing_password(password) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('UTF-8'), salt)
    return hashed.decode('UTF-8')


async def verify_password(password, hash_password) -> bool:
    return bcrypt.checkpw(password.encode('UTF-8'), hash_password.encode('UTF-8'))


async def generate_jwt(data: dict) -> str:
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({'exp': expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITH)
    return token


@auth.post('/registration', status_code=201)
async def registration(user: CreateUser, db: AsyncSession = Depends(get_session)) -> dict:
    password = await hashing_password(user.password)
    new_user = Users(username=user.username, email=user.email, password=password)
    try:
        db.add(new_user)
        await db.commit()
        return {'message': 'Success'}
    except:
        raise HTTPException(status_code=409, detail='user is exist')


@auth.post('/login', status_code=200)
async def login(username: str = Form(...), password: str = Form(...)) -> dict:
    user = await get_user_by_username(username)
    if user:
        if await verify_password(password, user.password):
            token = await generate_jwt({'sub': user.username})
            return {'token': token, 'type': 'bearer'}
    raise HTTPException(status_code=400, detail='invalid username or password')


@auth.get('/me', status_code=200)
async def get_ifo_about_me(user: Users = Depends(get_user_by_jwt)):
    return user


@auth.delete('/remove', status_code=200)
async def delete(user: Users = Depends(get_user_by_jwt), db: AsyncSession = Depends(get_session)) -> dict:
    await db.delete(user)
    await db.commit()
    return {'message': 'Success'}
