# import asyncio
# import sys
from http import HTTPStatus

from fastapi import FastAPI
from starlette.responses import HTMLResponse

from fast_zero.routers import auth, local, todos, users
from fast_zero.schemas import (
    Message,
)

# Caso esteja executando em terminal do windows,
# é necessário usar o WindowsSelectorEventLoopPolicy para evitar erros
# relacionados ao loop de eventos do asyncio.
# O código abaixo verifica se o sistema operacional é Windows e,
# se for, define a política de loop de eventos apropriada.
# if sys.platform == 'win32':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(local.router)

app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}


@app.get('/exercise-html', response_class=HTMLResponse)
def exercise_html():
    return """
    <html>
        <head>
            <title>Our Hello World</title>
        </head>
        <body>
            <h1>Hello World</h1>
        </body>
    </html>
    """
