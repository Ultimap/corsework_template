from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import auth
from routers.category import category
from routers.items import items
from models import Base
from database import async_session
from fastapi.responses import FileResponse
from settings import img_folder
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/img/{img_name}', status_code=200)
async def get_img(img_name: str):
    return FileResponse(f"{img_folder}/{img_name}")

app.include_router(auth)
app.include_router(category)
app.include_router(items)
