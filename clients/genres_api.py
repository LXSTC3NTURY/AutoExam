from config.base_urls import MOVIES_BASE_URL
from custom_requester.custom_requester import CustomRequester


class GenresApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_genres(self, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint="/genres",
            expected_status=expected_status
        )
