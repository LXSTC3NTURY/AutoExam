import pytest
from conftest import generate_user_data


class TestAuth:
    def test_register_user(self, api_manager, test_user):
        """Verifies successful user registration: response contains matching email, id, and the USER role."""
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        assert "id" in response_data
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, api_manager, registered_user):
        """Verifies that a registered user can log in and receives an access token."""
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]

    def test_get_user_info_without_auth(self, unauthenticated_api_manager):
        """Verifies that requesting user info without an Authorization header returns 401."""
        user_api = unauthenticated_api_manager.user_api
        assert "Authorization" not in user_api.session.headers
        user_api.get_user_info("me", expected_status=401)

    def test_get_user_info_forbidden_for_regular_user(self, api_manager, authenticated_user):
        """Verifies that a regular USER cannot access GET /user/{id} (expects 403)."""
        user_id = authenticated_user["id"]
        response = api_manager.user_api.get_user_info(user_id, expected_status=403)
        assert response.status_code == 403, (
            f"Expected status 403 for a regular user, got {response.status_code}"
        )

    def test_bulk_delete_users(self, api_manager, admin_session):
        """Verifies that multiple users can be registered and then deleted in a single bulk request,
        and that none of the deleted users can log in afterwards."""
        users_data = [generate_user_data() for _ in range(3)]
        user_ids = []
        for user_data in users_data:
            response = api_manager.auth_api.register_user(user_data)
            assert response.status_code == 201, f"Registration failed: {response.status_code}"
            assert "id" in response.json(), "Response is missing 'id'"
            user_ids.append(response.json()["id"])

        api_manager.user_api.delete_users(*user_ids)

        for user_data in users_data:
            with pytest.raises(ValueError):
                api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))
