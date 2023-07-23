from uuid import UUID
from jose import jwt
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED

from src.core.config import settings


async def test_register_auth(app_instance: FastAPI, client: AsyncClient):
    register_r = await client.post(
        app_instance.url_path_for('register_user'),
        json={
            'username': 'test',
            'password': 'test',
        }
    )

    register_json: dict[str, str] = register_r.json()

    assert register_r.status_code == HTTP_201_CREATED
    assert register_json['username'] == 'test'
    assert register_json['password'] == 'test'
    assert register_json['created_at']
    assert UUID(register_json['id_user'])

    auth_r = await client.post(
        app_instance.url_path_for('auth_user'),
        json={
            'username': 'test',
            'password': 'test',
        },
    )

    token: str = auth_r.json()
    assert auth_r.status_code == HTTP_201_CREATED
    user_data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert user_data['username'] == 'test'
    assert user_data['password'] == 'test'
    assert user_data['id'] == register_json['id_user']


async def test_register_auth_exc(app_instance: FastAPI, client: AsyncClient):
    await client.post(
        app_instance.url_path_for('register_user'),
        json={
            'username': 'test2',
            'password': 'test2',
        }
    )

    auth_r = await client.post(
        app_instance.url_path_for('auth_user'),
        json={
            'username': 'test2',
            'password': 'abracadabra',
        }
    )
    auth_json: dict[str, str] = auth_r.json()
    assert auth_r.status_code == HTTP_404_NOT_FOUND
    assert auth_json['detail'] == 'Wrong username/password'


