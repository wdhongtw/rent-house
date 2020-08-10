import requests
from typing import TypedDict

class House():
    name: str
    url: str
    cost: int

    def __init__(self, name: str, url: str, cost: int):
        self.name = name
        self.url = url
        self.cost = cost


_ifttt_webhook_fmt = 'https://maker.ifttt.com/trigger/{}/with/key/{}'


class Notifier():
    _token: str
    _event_name: str = 'new_house'

    def __init__(self, token: str):
        self._token = token

    def notify_new_house(self, house: House):
        url = _ifttt_webhook_fmt.format(self._event_name, self._token)
        response = requests.post(url, json={
            "value1": house.name,
            "value2": str(house.cost),
            "value3": house.url,
        })
        response.raise_for_status()
