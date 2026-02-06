from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_should_return_hello_world():
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act - Executa a coisa (o SUT)
    - A: Assert - Garanta que A é A
    """
    # arrange
    client = TestClient(app)

    # ACT
    response = client.get('/')

    # Assert
    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK


def test_exercise_html():
    client = TestClient(app)
    response = client.get('/exercise-html')
    assert '<h1>Hello World</h1>' in response.text
    assert response.status_code == HTTPStatus.OK
