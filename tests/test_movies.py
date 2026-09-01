import requests
from custom_requester.custom_requester import CustomRequester

def test_movies():
    params = {
        "pageSize": 10,
        "page": 1,
        "minPrice": 1,
        "maxPrice": 1000,
        "locations": ["MSK", "SPB"],
        "published": True,
        "genreId": 9,
        "createdAt": "asc",
        }
    session = requests.Session()
    requester = CustomRequester(session=session, base_url="https://api.dev-cinescope.coconutqa.ru")

    response = requester.send_request(
    "GET",
    "/movies",
    params=params
)

    body = response.json()
    movies = body["movies"]
    assert movies, "Список фильмов пуст — нечего проверять"

    for movie in movies:
        assert movie["genreId"] == params["genreId"], f"Фильм id={movie['id']}: ожидали жанр {params['genreId']}, получили {movie['genreId']}"

