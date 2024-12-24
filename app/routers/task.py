from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task
from app.models import User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router_task = APIRouter(prefix='/task', tags=['task'])


@router_task.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router_task.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=404, detail='Task was not found')
    return task


@router_task.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_tsk: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(insert(Task).values(title=create_tsk.title,
                                       content=create_tsk.content,
                                       priority=create_tsk.priority,
                                       slug=slugify(create_tsk.title),
                                       user_id=user_id))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    else:
        raise HTTPException(status_code=404, detail='User was not found')


@router_task.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_tsk: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=404, detail='Task was not found')
    db.execute(update(Task).where(Task.id == task_id).values(title=create_task.title,
                                                             content=create_task.content,
                                                             priority=create_task.priority))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}


@router_task.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=404, detail='Task was not found')
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}
