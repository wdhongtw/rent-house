import typing
import logging

import requests

from fetcher import House, Notifier, UrlGenerator


_ifttt_webhook_fmt = "https://maker.ifttt.com/trigger/{}/with/key/{}"


class EmptyNotifier(Notifier):
    def notify(self, house: House) -> None:
        pass


class IftttNotifier(Notifier):
    _token: str
    _event_name: str
    _url_func: typing.Tuple[UrlGenerator]
    _logger: logging.Logger

    def __init__(
        self, logger: logging.Logger, url_func: UrlGenerator, token: str, event: str,
    ) -> None:
        self._token = token
        self._event_name = event
        self._url_func = (url_func,)
        self._logger = logger

    def notify(self, house: House) -> None:
        url = _ifttt_webhook_fmt.format(self._event_name, self._token)
        self._logger.info("Notify new house %s", house.description)
        response = requests.post(
            url,
            json={
                "value1": "{} {} - {}".format(
                    house.region, house.section, house.description
                ),
                "value2": "{} {} - {}".format(
                    house.price_value, house.price_unit, house.area
                ),
                "value3": self._url_func[0](house),
            },
        )
        if response.status_code != 200:
            self._logger.error(
                "Fail to notify new house %s: HTTP %d",
                house.description,
                response.status_code,
            )
