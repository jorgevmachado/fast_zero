from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import Todo, User


@pytest.mark.asyncio
async def test_create_user_db(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'email': 'teste@test',
        'username': 'alice',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
        'todos': [],
    }


@pytest.mark.asyncio
async def test_create_todo(session, user: User, mock_db_time):
    with mock_db_time(model=Todo) as time:
        new_todo = Todo(
            title='Test Todo',
            state='draft',
            user_id=user.id,
            description='Test Desc',
        )
        session.add(new_todo)
        await session.commit()

    todo = await session.scalar(select(Todo).where(Todo.title == 'Test Todo'))

    assert asdict(todo) == {
        'id': 1,
        'state': 'draft',
        'title': 'Test Todo',
        'user_id': 1,
        'created_at': time,
        'updated_at': time,
        'description': 'Test Desc',
    }


@pytest.mark.asyncio
async def test_user_todo_relationship(session, user: User):
    todo = Todo(
        title='Test Todo',
        state='draft',
        user_id=user.id,
        description='Test Desc',
    )

    session.add(todo)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))

    assert user.todos == [todo]
