from http import HTTPStatus


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
