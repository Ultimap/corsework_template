from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from settings import DATABASE_URL, SECRET_KEY, ALGORITH, oauth2scheme
from sqlalchemy import select
from models import Users, Category, Roles, Items
import jwt
from fastapi import Depends, HTTPException

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session


async def get_user_by_username(username: str) -> Users:
    async with async_session() as db:
        user = await db.execute(select(Users).where(Users.username == username))
        return user.scalar_one_or_none()


async def verify_token(token: str):
    try:
        decode_data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITH)
        return decode_data
    except jwt.PyJWTError:
        return None


async def get_user_by_jwt(token: str = Depends(oauth2scheme)):
    decode_data = await verify_token(token)
    print(decode_data)
    if not decode_data:
        raise HTTPException(status_code=400, detail='invalid token')
    user = await get_user_by_username(decode_data['sub'])
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    return user


async def get_category_by_id(id: int, db: AsyncSession):
    category = await db.execute(select(Category).where(Category.id == id))
    return category.scalar_one_or_none()


async def get_item_by_id(id: int, db: AsyncSession):
    item = await db.execute(select(Items).where(Items.id == id))
    return item.scalar_one_or_none()


async def get_role_by_user(user: Users, db: AsyncSession):
    role = await db.execute(select(Roles).where(Roles.id == user.role_id))
    role_name = role.scalar_one_or_none().name
