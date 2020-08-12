import json
import logging
import math

import requests
from bs4 import BeautifulSoup
import typing


QueryOptions = typing.Dict[str, typing.Union[typing.List[str], str]]


class House:
    post_id: int

    region: str
    section: str
    description: str
    price_value: int
    price_unit: str
    area: int
    refresh_time: int

    raw_data: str

    def __init__(self):
        pass

    @classmethod
    def from_json(cls, source) -> "House":
        house = cls()
        house.post_id = source["post_id"]
        house.region = source["region_name"]
        house.section = source["section_name"]
        house.description = source["fulladdress"]
        house.price_value = int(source["price"].replace(",", ""))
        house.price_unit = source["unit"]
        house.area = source["area"]
        house.refresh_time = source["refreshtime"]

        house.raw_data = json.dumps(source)
        return house


class Fetcher:
    """Fetch house information from 591."""

    _root_url: str = "https://rent.591.com.tw/"
    _api_url: str = "https://rent.591.com.tw/home/search/rsList"
    _house_url_fmt: str = "https://rent.591.com.tw/rent-detail-{}.html"

    __static_options: QueryOptions = {
        "is_new_list": "1",
        "type": "1",
        "searchtype": "1",
    }

    _logger: logging.Logger

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger
        self._session = requests.Session()
        self.__make_headers()

    def __make_headers(self) -> None:
        response = self._session.get(self._root_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.select("meta"):
            if tag.get("name", None) == "csrf-token":
                csrf_token = tag.get("content")
                self._session.headers["X-CSRF-TOKEN"] = csrf_token
                break
        else:
            raise RuntimeError("No CSRF token found")

        self._logger.info("Find CSRF token: %s", csrf_token)

    def get_total(self, query_options: QueryOptions) -> int:
        """Check total house counts for given query option."""
        options = {**self.__static_options, **query_options}

        response = self._session.get(self._api_url, params=options)
        response.raise_for_status()

        counts = int(response.json()["records"])
        return counts

    def __get_houses(self, options: QueryOptions) -> typing.Iterable[House]:
        response = self._session.get(self._api_url, params=options)
        response.raise_for_status()

        data = response.json()["data"]
        houses = data.get("data", [])
        for house in houses:
            yield House.from_json(house)

    def get_houses(self, query_options: QueryOptions) -> typing.Iterable[House]:
        """Generate houses from specified search option."""
        counts = self.get_total(query_options)
        pages = math.ceil(counts / 30)
        self._logger.info("Find %d houses, %d pages", counts, pages)

        for page in range(pages):
            options = {**self.__static_options, **query_options}
            options["firstRow"] = str(30 * page)

            for house in self.__get_houses(options):
                yield house
