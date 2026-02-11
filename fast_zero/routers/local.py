from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

router = APIRouter(prefix='/local', tags=['local'])


# Esté ponto do código foi mantido para fins de entendimento,
# no caso agora é realizado através de conexão com banco de dados
database = []


@router.post(
    '/users', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def local_create_user(user: UserSchema):
    # user_with_id = UserDB(
    #     username=user.username,
    #     email=user.email,
    #     password=user.password,
    #     id=len(database) + 1
    # )
    # Forma simplificada
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@router.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def local_read_users():
    return {'users': database}


@router.put('/users/{user_id}', response_model=UserPublic)
def local_update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@router.delete('/users/{user_id}', response_model=Message)
def local_delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    del database[user_id - 1]

    return {'message': 'User deleted'}


@router.get('/users/{user_id}', response_model=UserPublic)
def local_get_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return database[user_id - 1]
