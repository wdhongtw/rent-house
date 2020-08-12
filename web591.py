"""Module for 591 crawler."""

import argparse
import logging

import toml

import fetcher


logger = logging.getLogger("crawler")
log_formatter = logging.Formatter(
    fmt="%(asctime)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", dest="config", required=True, help="The configuration file"
    )
    args = vars(parser.parse_args())

    settings = toml.load(args["config"])

    agent = fetcher.Fetcher(logger)
    houses = list(agent.get_houses(settings["query"]))
    _ = houses


if __name__ == "__main__":
    main()
