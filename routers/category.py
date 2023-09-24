from fastapi import APIRouter, Depends, HTTPException
from database import get_session, get_category_by_id, get_role_by_user, get_user_by_jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from models import Category, Users
from sqlalchemy import select
category = APIRouter(prefix='/category', tags=['Category'])


class CategoryScheme(BaseModel):
    name: str


@category.get('', status_code=200)
async def get_categories(db: AsyncSession = Depends(get_session)):
    categories = await db.execute(select(Category))
    return categories.scalars().all()


@category.post('/add', status_code=201)
async def create(name: CategoryScheme,db: AsyncSession = Depends(get_session),
                 # user: Users = Depends(get_user_by_jwt)
                 ) -> dict:
    # role = await get_role_by_user(user, db)
    # if role in ('admin', 'manager'):
        try:
            new_category = Category(name=name.name)
            db.add(new_category)
            await db.commit()
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409, detail='category is exist')
    # raise HTTPException(status_code=403, detail='Forbidden')


@category.put('/{id}/edit', status_code=200)
async def edit(id: int,name: CategoryScheme, db: AsyncSession = Depends(get_session), user: Users = Depends(get_user_by_jwt)) -> dict:
    role = await get_role_by_user(user, db)
    if role in ('admin', 'manager'):
        edit_category = await get_category_by_id(id, db)
        if not edit_category:
            raise HTTPException(status_code=404, detail='category not found')
        edit_category.name = name.name
        await db.commit()
        return {'message': 'Success'}
    raise HTTPException(status_code=403, detail='Forbidden')


@category.delete('/{id}/delete', status_code=200)
async def delete(id: int, db: AsyncSession = Depends(get_session), user: Users = Depends(get_user_by_jwt)) -> dict:
    role = await get_role_by_user(user, db)
    if role in ('admin', 'manager'):
        delete_category = await get_category_by_id(id, db)
        if not category:
            raise HTTPException(status_code=404, detail='category not found')
        await db.delete(delete_category)
        await db.commit()
        return {'message': 'Success'}
    raise HTTPException(status_code=403, detail='Forbidden')
