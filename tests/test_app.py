from http import HTTPStatus


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
