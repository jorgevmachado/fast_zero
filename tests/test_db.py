from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User


def test_create_user_db(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'email': 'teste@test',
        'username': 'alice',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }
