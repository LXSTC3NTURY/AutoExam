from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_BASE_URL

MOVIES = "/movies"
MOVIE_BY_ID = '/movies/{id}'


class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_movies(self, params=None, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=MOVIES,
            params=params,
            expected_status=expected_status,
            **kwargs
        )

    def get_movie_by_id(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=MOVIE_BY_ID.format(id=movie_id),
            expected_status=expected_status,
            **kwargs
        )

    def create_movie(self, movie_data, expected_status=201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=MOVIES,
            data=movie_data,
            expected_status=expected_status,
            **kwargs
        )

    def update_movie(self, movie_id, movie_data, expected_status=200, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=MOVIE_BY_ID.format(id=movie_id),
            data=movie_data,
            expected_status=expected_status,
            **kwargs
        )

    def delete_movie(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=MOVIE_BY_ID.format(id=movie_id),
            expected_status=expected_status,
            **kwargs
        )
