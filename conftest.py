import requests
import pytest
from faker.generator import random

from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator


@pytest.fixture(scope="class")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="class")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="function")
def test_user():
    return generate_user_data()


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user


@pytest.fixture(scope="class")
def unauthenticated_api_manager():
    http_session = requests.Session()
    yield ApiManager(http_session)
    http_session.close()


@pytest.fixture(scope="function")
def authenticated_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    test_user["id"] = response.json()["id"]
    api_manager.auth_api.authenticate((test_user["email"], test_user["password"]))
    return test_user


def generate_user_data():
    password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="function")
def admin_user():
    return {
        "email": "api1@gmail.com",
        "password": "asdqwe123Q"
    }


@pytest.fixture(scope="function")
def admin_session(api_manager, admin_user):
    api_manager.auth_api.authenticate((admin_user["email"], admin_user["password"]))
    return api_manager


@pytest.fixture(scope="function")
def existing_genre_id(api_manager):
    response = api_manager.genres_api.get_genres()
    genres = response.json()
    assert len(genres) > 0, "В системе нет ни одного жанра — нечего выбирать"
    return random.choice(genres)["id"]


def generate_movie_data(genre_id):
    return {
        "name": DataGenerator.generate_movie_name(),
        "imageUrl": DataGenerator.generate_image_url(),
        "price": DataGenerator.generate_total_price(),
        "description": DataGenerator.generate_movie_description(),
        "location": DataGenerator.generate_location(),
        "published": True,
        "genreId": genre_id
    }


@pytest.fixture(scope="function")
def movie_data(existing_genre_id):
    return generate_movie_data(existing_genre_id)


@pytest.fixture(scope="function")
def updated_movie_data(existing_genre_id):
    return generate_movie_data(existing_genre_id)


@pytest.fixture(scope="function")
def created_movie(api_manager, admin_session, movie_data):
    response = api_manager.movies_api.create_movie(movie_data)
    return response.json()
