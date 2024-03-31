from locust import HttpUser, between, task


class UGCTest(HttpUser):
    wait_time = between(1, 5)

    @task(100)
    def custom_event(self):
        data = {
            "user_uuid": "1234",
            "event_type": "1234",
            "timestamp": "1234"
        }
        self.client.post("http://localhost:5555/ugc/v1/custom_event", data)

    @task(100)
    def player_event(self):
        data = {
            "user_uuid": "1234",
            "film_uuid": "1234",
            "event_type": "seek",
            "event_value": "1234",
            "timestamp": "1234"
        }
        self.client.post("http://localhost:5555/ugc/v1/player_event", data)

    @task(100)
    def view_event(self):
        data = {
            "user_uuid": "1234",
            "film_uuid": "1234"
        }
        self.client.post("http://localhost:5555/ugc/v1/view_event", data)
