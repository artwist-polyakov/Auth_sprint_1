# from locust import HttpUser, between, task
# class UGCTest(HttpUser):
#     wait_time = between(1, 5)

    # @task
    # def custom_event(self):
    #     # data = {
    #     #     "user_uuid": "1234",
    #     #     "event_type": "1234",
    #     #     "timestamp": 1234
    #     # }
    #     self.client.post("/ugc/v1/custom_event?user_uuid=1234&event_type=1234&timestamp=1234")
    #
    # @task(100)
    # def player_event(self):
    #     data = {
    #         "user_uuid": "1234",
    #         "film_uuid": "1234",
    #         "event_type": "seek",
    #         "event_value": "1234",
    #         "timestamp": "1234"
    #     }
    #     with self.client.post(
    #             "/ugc/v1/player_event",
    #             data=data,
    #             catch_response=True
    #     ) as response:
    #         print(response)
    #
    #
    #
    #
    #         #
    # # @task(100)
    # # def view_event(self):
    # #     data = {
    # #         "user_uuid": "1234",
    # #         "film_uuid": "1234"
    # #     }
    # #     self.client.post("/ugc/v1/view_event", data=data)
    #
    # # @task
    # # def viewCart(self):
    # #     with self.client.post(
    # #             "ugc/v1/custom_event?user_uuid=1234&event_type=1234&timestamp=1234",
    # #             catch_response=True
    # #     ) as response:
    # #         print(f"{response.json()}")
    # #         # if '"prod_id":1' not in response.text:
    # #         #     response.failure("Assert failure, response does not contain expected prod_id")



import requests


url = "http://localhost:5555/ugc/v1/custom_event?user_uuid=1234&event_type=1234&timestamp=1234"

requests = requests.post(url)

print(requests)
