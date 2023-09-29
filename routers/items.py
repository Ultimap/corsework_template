from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_session, get_item_by_id, get_category_by_id, get_user_by_jwt, get_role_by_user
from models import Items
from typing import Dict
from pydantic import Json
from models import Users
from settings import img_folder
import os
items = APIRouter(prefix='/items', tags=['Items'])


@items.get('', status_code=200)
async def get_items(db: AsyncSession = Depends(get_session)):
    items_all = await db.execute(select(Items))
    return items_all.scalars().all()


@items.get('/{id}', status_code=200)
async def get_item(id: int, db: AsyncSession = Depends(get_session)):
    item = await get_item_by_id(id, db)
    if not item:
        raise HTTPException(status_code=404, detail='item not found')
    category = await get_category_by_id(item.category, db)
    return {**item.__dict__, 'category': category.name}


@items.post('/add', status_code=201)
async def create(
        name: str = Form(...),
        img: UploadFile = File(...),
        description: str = Form(...),
        characteristics: str = Form(...),
        quantity: int = Form(...),
        cost: int = Form(...),
        category_id: int = Form(...),
        db: AsyncSession = Depends(get_session),
        user: Users = Depends(get_user_by_jwt)
) -> dict:
    if user.role_id == 1:
        item = Items(name=name, img=img.filename, description=description, characteristics=characteristics,
                     quantity=quantity, cost=cost, category=category_id)
        try:
            db.add(item)
            await db.commit()
            os.makedirs(img_folder, exist_ok=True)
            img_path = os.path.join(img_folder, img.filename)
            with open(img_path, 'wb') as file:
                content = await img.read()
                file.write(content)
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409, detail='item is exist')
    raise HTTPException(status_code=403, detail='Forbidden')


@items.delete('/{id}/delete', status_code=200)
async def delete(id: int, db: AsyncSession = Depends(get_session), user: Users = Depends(get_user_by_jwt)):
    if user.role_id == 2:
        item = await get_item_by_id(id, db)
        print(item.name)
        if item:
            await db.delete(item)
            await db.commit()
            return {'message': 'Success'}
        raise HTTPException(status_code=404, detail='item not found')
    raise HTTPException(status_code=403, detail='Forbidden')

