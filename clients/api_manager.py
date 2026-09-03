from clients.auth_api import AuthApi
from clients.user_api import UserApi
from clients.genres_api import GenresApi
from clients.movies_api import MoviesApi


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthApi(session)
        self.user_api = UserApi(session)
        self.genres_api = GenresApi(session)
        self.movies_api = MoviesApi(session)
