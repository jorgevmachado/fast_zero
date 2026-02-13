from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import String, cast, select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    FilterTodo,
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fast_zero.security import get_current_user

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=TodoPublic)
async def create_todo(todo: TodoSchema, user: CurrentUser, session: Session):
    db_todo = Todo(
        title=todo.title,
        state=todo.state,
        user_id=user.id,
        description=todo.description,
    )

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
async def list_todos(
    session: Session,
    user: CurrentUser,
    todo_filter: Annotated[FilterTodo, Query()],
):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )

    if todo_filter.state:
        query = query.filter(
            cast(Todo.state, String).contains(todo_filter.state)
        )

    todos = await session.scalars(
        query.offset(todo_filter.skip).limit(todo_filter.limit)
    )

    return {'todos': todos.all()}


@router.get('/{todo_id}', response_model=TodoPublic)
async def get_todo(todo_id: int, session: Session, user: CurrentUser):
    db_todo = await session.scalar(
        select(Todo).where(Todo.id == todo_id).where(Todo.user_id == user.id)
    )

    if not db_todo:
        raise HTTPException(
            detail='Task not found.',
            status_code=HTTPStatus.NOT_FOUND,
        )

    return db_todo


@router.patch('/{todo_id}', response_model=TodoPublic)
async def patch_todo(
    todo_id: int, session: Session, user: CurrentUser, todo: TodoUpdate
):
    db_todo = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    # É o mesmo que os filtros do list_todos,
    # só que ao invés de fazer if por if, ele faz como um loop
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
async def delete_todo(
    todo_id: int,
    session: Session,
    user: CurrentUser,
):
    db_todo = await session.scalar(
        select(Todo).where(Todo.id == todo_id).where(Todo.user_id == user.id)
    )

    if not db_todo:
        raise HTTPException(
            detail='Task not found.',
            status_code=HTTPStatus.NOT_FOUND,
        )

    await session.delete(db_todo)
    await session.commit()

    return {'message': 'Task has been deleted successfully.'}
