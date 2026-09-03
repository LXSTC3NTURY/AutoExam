import pytest


@pytest.mark.api
@pytest.mark.movies
class TestMovies:
    def test_get_movies_without_filters(self, api_manager):
        """Verifies that GET /movies without parameters returns 200 and a correct response structure."""
        response = api_manager.movies_api.get_movies()
        body = response.json()
        expected_keys = ["movies", "count", "page", "pageSize", "pageCount"]
        for key in expected_keys:
            assert key in body, f"Response is missing key '{key}'. Received: {list(body.keys())}"

        assert isinstance(body["movies"], list), (
            f"Expected 'movies' to be a list, got {type(body['movies'])}"
        )

    def test_get_movies_filtered_by_genre(self, api_manager, existing_genre_id):
        """Verifies that filtering by genreId returns only movies of that genre."""
        params = {"genreId": existing_genre_id}
        response = api_manager.movies_api.get_movies(params=params)
        body = response.json()
        movies = body["movies"]

        for movie in movies:
            assert movie["genreId"] == existing_genre_id, (
                f"Movie id={movie['id']}: expected genre {existing_genre_id}, got {movie['genreId']}"
            )

    def test_get_movie_by_id(self, api_manager, admin_session, movie_data, created_movie):
        """Verifies that a created movie can be retrieved by ID: status 200 and fields matching the original data."""
        movie_id = created_movie["id"]

        response = api_manager.movies_api.get_movie_by_id(movie_id)

        body = response.json()
        assert body["id"] == movie_id, f"Expected id={movie_id}, got {body['id']}"
        assert body["name"] == movie_data["name"], (
            f"Expected name='{movie_data['name']}', got '{body['name']}'"
        )
        assert body["price"] == movie_data["price"], (
            f"Expected price={movie_data['price']}, got {body['price']}"
        )
        assert body["description"] == movie_data["description"], (
            f"Expected description='{movie_data['description']}', got '{body['description']}'"
        )
        assert body["location"] == movie_data["location"], (
            f"Expected location='{movie_data['location']}', got '{body['location']}'"
        )
        assert body["genreId"] == movie_data["genreId"], (
            f"Expected genreId={movie_data['genreId']}, got {body['genreId']}"
        )

    def test_get_movie_by_id_not_found(self, api_manager):
        """Verifies that requesting a non-existent movie by ID returns 404."""
        non_existent_id = 999999999
        api_manager.movies_api.get_movie_by_id(non_existent_id, expected_status=404)

    def test_create_movie(self, api_manager, admin_session, movie_data):
        """Verifies successful movie creation (happy path): status 201 and correctness of all fields in the response."""
        response = api_manager.movies_api.create_movie(movie_data)
        body = response.json()
        fields_to_check = ["name", "price", "description", "location", "published", "genreId"]

        for field in fields_to_check:
            assert body[field] == movie_data[field], (
                f"Field '{field}': expected {movie_data[field]}, got {body[field]}"
            )

        assert "id" in body, f"Response is missing key 'id'. Received: {list(body.keys())}"
        assert "createdAt" in body, f"Response is missing key 'createdAt'. Received: {list(body.keys())}"

    def test_created_movie_is_retrievable(self, api_manager, admin_session, movie_data, created_movie):
        """Verifies that a created movie is actually persisted and retrievable via a separate GET request."""
        movie_id = created_movie["id"]
        get_response = api_manager.movies_api.get_movie_by_id(movie_id)
        get_response_body = get_response.json()
        assert get_response_body["name"] == movie_data["name"], (
            f"Movie name mismatch: expected '{movie_data['name']}', got '{get_response_body['name']}'"
        )

    def test_create_movie_forbidden_for_regular_user(self, api_manager, authenticated_user, movie_data):
        """Verifies that a regular USER cannot create a movie (expects 403)."""
        api_manager.movies_api.create_movie(movie_data, expected_status=403)

    def test_create_movie_duplicate_name(self, api_manager, admin_session, movie_data):
        """Verifies that creating a movie with a name that already exists returns 409."""
        api_manager.movies_api.create_movie(movie_data)
        api_manager.movies_api.create_movie(movie_data, expected_status=409)

    def test_create_movie_invalid_genre_id(self, api_manager, admin_session, movie_data):
        """Verifies that creating a movie with a non-existent genreId returns 400."""
        movie_data["genreId"] = 999999999
        api_manager.movies_api.create_movie(movie_data, expected_status=400)

    def test_update_movie(self, api_manager, admin_session, created_movie, updated_movie_data):
        """
        Verifies successful movie update via PATCH: status 200,
        correctness of fields in the PATCH response, and confirms the changes via a separate GET.
        """
        movie_id = created_movie["id"]
        update_response = api_manager.movies_api.update_movie(movie_id, updated_movie_data)
        fields_to_check = ["name", "price", "description", "location", "published", "genreId"]
        updated_body = update_response.json()

        for field in fields_to_check:
            assert updated_body[field] == updated_movie_data[field], (
                f"Field '{field}' in PATCH response: expected {updated_movie_data[field]}, got {updated_body[field]}"
            )

        get_response = api_manager.movies_api.get_movie_by_id(movie_id)
        get_body = get_response.json()
        for field in fields_to_check:
            assert get_body[field] == updated_movie_data[field], (
                f"Field '{field}' after GET: expected {updated_movie_data[field]}, got {get_body[field]}"
            )

    def test_update_movie_invalid_genre_id(self, api_manager, admin_session, created_movie, updated_movie_data):
        """
        Verifies that updating a movie with a non-existent genreId returns 404.

        Note: the API returns statusCode 404 with message "Фильм не найден" (Movie not found)
        for this case, even though the movie itself exists — the actual issue is the invalid
        genreId, not a missing movie. This looks like a misleading error message and may be
        worth reporting as a bug.
        """
        movie_id = created_movie["id"]
        updated_movie_data["genreId"] = 999999999
        api_manager.movies_api.update_movie(movie_id, updated_movie_data, expected_status=404)

    def test_update_movie_forbidden_for_regular_user(
            self, api_manager, created_movie, authenticated_user, updated_movie_data ):
        """Verifies that a regular USER cannot update a movie (expects 403)."""
        movie_id = created_movie["id"]
        api_manager.movies_api.update_movie(movie_id, updated_movie_data, expected_status=403)

    def test_update_movie_not_found(self, api_manager, admin_session, updated_movie_data):
        """Verifies that updating a non-existent movie returns 404."""
        non_existent_id = 999999999
        api_manager.movies_api.update_movie(non_existent_id, updated_movie_data, expected_status=404)

    def test_delete_movie(self, api_manager, admin_session, created_movie):
        """Verifies successful movie deletion: the movie becomes inaccessible after deletion."""
        movie_id = created_movie["id"]

        api_manager.movies_api.delete_movie(movie_id)
        api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)

    def test_delete_movie_not_found(self, api_manager, admin_session):
        """Verifies that deleting a non-existent movie returns 404."""
        non_existent_id = 999999999

        api_manager.movies_api.delete_movie(non_existent_id, expected_status=404)

    def test_delete_movie_forbidden_for_regular_user(self, api_manager, created_movie, authenticated_user):
        """Verifies that a regular USER cannot delete a movie (expects 403)."""
        movie_id = created_movie["id"]
        api_manager.movies_api.delete_movie(movie_id, expected_status=403)
