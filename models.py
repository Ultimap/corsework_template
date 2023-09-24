from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()


class Roles(Base):
    __tablename__ = 'Roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Users(Base):
    __tablename__ = 'Users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=False)
    role_id = Column(ForeignKey(Roles.id), default=1)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Items(Base):
    __tablename__ = 'Items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    img = Column(String, default='placeholder.png')
    description = Column(Text, nullable=True)
    characteristics = Column(String)
    quantity = Column(Integer, default=0)
    cost = Column(Integer, default=0)
    category = Column(ForeignKey(Category.id))


class UserItem(Base):
    __tablename__ = 'UserItem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(ForeignKey(Users.id))
    item = Column(ForeignKey(Items.id))
