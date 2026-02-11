from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_should_unauthorized_when_not_user_found(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'not-user', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_should_unauthorized_when_password_invalid(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'password-weak'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
