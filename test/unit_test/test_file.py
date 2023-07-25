from pathlib import Path

from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
import pytest


@pytest.fixture(scope='session')
def test_file_path() -> str:
    filename = 'test.txt'

    with open(filename, 'w') as f:
        f.write('abracadabra')

    p = Path().cwd() / filename
    return str(p)


@pytest.fixture(scope='session')
async def user_token(app_instance: FastAPI, client: AsyncClient) -> str:
    await client.post(
        app_instance.url_path_for('register_user'),
        json={
            'username': 'test_file',
            'password': 'test_file',
        }
    )

    auth_r = await client.post(
        app_instance.url_path_for('auth_user'),
        json={
            'username': 'test_file',
            'password': 'test_file',
        }
    )
    return auth_r.json()


async def test_upload_file(app_instance: FastAPI, client: AsyncClient, user_token: str, test_file_path: str):
    with open(test_file_path, 'rb') as f:
        response = await client.post(
            app_instance.url_path_for('upload_file') + '?path=test/',
            files={'file': f},
            headers={'Authorization': f'Bearer {user_token}'},
        )
    resp_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert resp_json['created_at']
    assert resp_json['id_file']
    assert resp_json['is_downloadable'] is True
    assert resp_json['name'] == 'test.txt'
    assert resp_json['path'] == 'test/test.txt'
    assert resp_json['size'] == 11


async def test_upload_file_by_fullpath(
        app_instance: FastAPI,
        client: AsyncClient,
        user_token: str,
        test_file_path: str
):
    with open(test_file_path, 'rb') as f:
        response = await client.post(
            app_instance.url_path_for('upload_file') + '?path=test/123.txt',
            files={'file': f},
            headers={'Authorization': f'Bearer {user_token}'},
        )
    resp_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert resp_json['created_at']
    assert resp_json['id_file']
    assert resp_json['is_downloadable'] is True
    assert resp_json['name'] == '123.txt'
    assert resp_json['path'] == 'test/123.txt'
    assert resp_json['size'] == 11


async def test_get_files_info(app_instance: FastAPI, client: AsyncClient, user_token: str, test_file_path: str):
    with open(test_file_path, 'rb') as f:
        await client.post(
            app_instance.url_path_for('upload_file') + '?path=test/get_file.txt',
            files={'file': f},
            headers={'Authorization': f'Bearer {user_token}'},
        )

    response = await client.get(
        app_instance.url_path_for('get_files'),
        headers={'Authorization': f'Bearer {user_token}'},
    )

    resp_json = response.json()
    file_names = {file['name'] for file in resp_json}
    assert 'get_file.txt' in file_names
    assert response.status_code == HTTP_200_OK


async def test_get_files_info_exc(app_instance: FastAPI, client: AsyncClient, user_token: str, test_file_path: str):
    with open(test_file_path, 'rb') as f:
        await client.post(
            app_instance.url_path_for('upload_file') + '?path=test/get_file_exc.txt',
            files={'file': f},
            headers={'Authorization': f'Bearer {user_token}'},
        )

    response = await client.get(
        app_instance.url_path_for('get_files'),
        headers={'Authorization': 'Bearer 123456'},
    )

    resp_json = response.json()
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert resp_json['detail'] == 'Authorization required'
