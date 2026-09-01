import pytest
import requests

from conftest import generate_user_data


class TestAuth:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        # добавим еше проверок
        assert "id" in response_data
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]

    def test_get_user_info_without_auth(self, unauthenticated_api_manager):
        user_api = unauthenticated_api_manager.user_api
        assert "Authorization" not in user_api.session.headers
        user_api.get_user_info("me", expected_status=401)

    def test_get_user_info(self, api_manager, authenticated_user):
        user_id = authenticated_user["id"]
        tested_email = authenticated_user["email"]
        tested_fullname = authenticated_user["fullName"]
        response = api_manager.user_api.get_user_info(user_id)
        assert response.json()["email"] == tested_email, (
            f"{response.json()["email"]} не совпадает с зарегистрированным {authenticated_user["email"]}"
        )
        assert response.json()["fullName"] == tested_fullname

    def test_bulk_delete_users(self, api_manager, admin_session):
        users_data = [generate_user_data() for _ in range(3)]
        user_ids = []
        for user_data in users_data:
            response = api_manager.auth_api.register_user(user_data)
            assert response.status_code == 201, f"Регистрация не удалась: {response.status_code}"
            assert "id" in response.json(), "В ответе нет id"
            user_ids.append(response.json()["id"])

        api_manager.user_api.delete_users(*user_ids)

        for user_data in users_data:
            with pytest.raises(ValueError):
                api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))



