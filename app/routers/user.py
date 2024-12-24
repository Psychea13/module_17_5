from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.models import Task
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router_user = APIRouter(prefix='/user', tags=['user'])


@router_user.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router_user.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    return user


@router_user.get('/user_id/tasks')
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id))
    return tasks


@router_user.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_new_user: CreateUser):
    db.execute(insert(User).values(username=create_new_user.username,
                                   firstname=create_new_user.firstname,
                                   lastname=create_new_user.lastname,
                                   age=create_new_user.age,
                                   slug=slugify(create_new_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router_user.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_us: UpdateUser):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    db.execute(update(User).where(User.id == user_id).values(
        username=update_us.username,
        firstname=update_us.firstname,
        lastname=update_us.lastname,
        age=update_us.age))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router_user.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    db.execute(delete(User).where(User.id == user_id))
    db.scalar(select(Task).where(Task.user_id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
