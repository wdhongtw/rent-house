"""Module for 591 crawler."""

import argparse
import logging
import typing

import toml

import fetcher
import store


logger = logging.getLogger("crawler")
log_formatter = logging.Formatter(
    fmt="%(asctime)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class Settings:
    core: typing.Dict[str, typing.Any]
    query: fetcher.QueryOptions
    storage: typing.Dict[str, typing.Any]

    def __init__(self, path):
        settings = toml.load(path)
        self.core = settings["core"]
        self.query = settings["query"]
        self.storage = settings["storage"]


def scan(settings: Settings):
    logger.warning("Scan houses from web site")
    storage: fetcher.HouseStore = store.LiteHouseStore(
        settings.storage["sqlite"]["path"]
    )
    agent = fetcher.Fetcher(logger, settings.core["page_delay"])
    scanner = fetcher.Scanner(logger, storage, agent, settings.core["batch_delay"])
    scanner.scan_house(settings.query)


def clean(settings: Settings):
    storage: fetcher.HouseStore = store.LiteHouseStore(
        settings.storage["sqlite"]["path"]
    )
    logger.warning("Clean all records in storage")
    for key in storage:
        del storage[key]


methods: typing.Dict[str, typing.Callable[[Settings], None]] = {
    "scan": scan,
    "clean": clean,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="591 crawling tool")
    parser.add_argument(
        "-c", dest="config", required=True, help="The configuration file"
    )
    parser.add_argument("action", help="The action to perform: scan, clean")
    args = vars(parser.parse_args())

    settings = Settings(args["config"])
    action = args["action"]

    handler = methods.get(action)
    if not handler:
        raise RuntimeError("no handler function")
    handler(settings)


if __name__ == "__main__":
    main()
