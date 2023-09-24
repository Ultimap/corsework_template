import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITH = os.environ['ALGORITHM']
oauth2scheme = OAuth2PasswordBearer('/auth/login')
img_folder = './img'
