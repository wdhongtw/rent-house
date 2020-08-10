#!/usr/bin/env python

import os

import ifttt


def _main():
    token = os.environ['TOKEN']
    notifier = ifttt.Notifier(token)
    notifier.notify_new_house(ifttt.House(
        name="天母",
        cost="30000",
        url="https://www.google.com/",
    ))
    print('Done')


if __name__ == "__main__":
    _main()

