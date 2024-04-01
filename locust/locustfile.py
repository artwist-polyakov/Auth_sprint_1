from locust import HttpUser, between, task


class UGCTest(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def custom_event(self):
        self.client.post(
            "/ugc/v1/custom_event"
            "?user_uuid=1234"
            "&event_type=1234"
            "&timestamp=1234"
        )

    @task(2)
    def player_event(self):
        self.client.post(
            "/ugc/v1/player_event"
            "?user_uuid=1234"
            "&film_uuid=1234"
            "&event_type=seek"
            "&event_value=1234"
            "&timestamp=1234"
        )

    @task(3)
    def view_event(self):
        self.client.post(
            "/ugc/v1/view_event"
            "?user_uuid=1234"
            "&film_uuid=1234"
        )
