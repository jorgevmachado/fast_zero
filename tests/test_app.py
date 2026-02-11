from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_should_return_hello_world(client):
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act - Executa a coisa (o SUT)
    - A: Assert - Garanta que A é A
    """
    # arrange: conftest.py

    # ACT
    response = client.get('/')

    # Assert
    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK


def test_exercise_html(client):
    response = client.get('/exercise-html')
    assert '<h1>Hello World</h1>' in response.text
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'email': 'alice@example.com',
            'username': 'alice',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_create_user_should_return_conflict_email_exists(client, user):
    response = client.post(
        '/users',
        json={
            'email': user.email,
            'username': 'fausto',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_should_return_conflict_username_exists(client, user):
    response = client.post(
        '/users',
        json={
            'email': 'email@example.com',
            'username': user.username,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_update_integrity_error(client, user, token):
    client.post(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'email': 'fausto@example.com',
            'username': 'fausto',
            'password': 'secret',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'email': 'fausto@example.com',
            'username': 'fausto',
            'password': 'secret',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_update_not_permission_error(client, user, token):
    response_update = client.put(
        '/users/3',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response_update.status_code == HTTPStatus.FORBIDDEN
    assert response_update.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_not_permission_error(client, user, token):
    response = client.delete(
        '/users/3',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_get_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'email': user.email,
        'username': user.username,
    }


def test_get_user_should_return_not_found(client):
    response = client.get('/users/666')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_local_create_user(client):
    response = client.post(
        '/local/users',
        json={
            'email': 'alice@example.com',
            'username': 'alice',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_local_read_users(client):
    response = client.get('/local/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'email': 'alice@example.com', 'username': 'alice'}]
    }


def test_local_update_user(client):
    response = client.put(
        '/local/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_local_get_user(client):
    response = client.get('/local/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_local_get_user_should_return_not_found(client):
    response = client.get('/local/users/666')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_local_update_user_should_return_not_found(client):
    response = client.put(
        '/local/users/666',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_local_delete_user(client):
    response = client.delete('/local/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_local_delete_user_should_return_not_found(client):
    response = client.delete('/local/users/666')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_should_unauthorized_when_not_user_found(client, user):
    response = client.post(
        '/token',
        data={'username': 'not-user', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_should_unauthorized_when_password_invalid(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': 'password-weak'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
