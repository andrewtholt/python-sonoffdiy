#!/usr/bin/env python3
# pylint: disable=W0621
"""Asynchronous Python client for Sonoff DIY device."""

import asyncio
import json
import sys
from time import sleep

from sonoffdiy import SonoffDIY


async def infoMain(loop):
    tryAgain = True
    count = 4

    while tryAgain:
        try:
            async with SonoffDIY(
                "192.168.10.169", device_id="1000c8c4b5", loop=loop
            ) as diy:
                info = await diy.update_info_json()
                print(info)
            tryAgain = False

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            tryAgain = False

        except SonoffDIYConnectionError:
            count -= 1
            tryAgain = True
            if count < 0:
                print("Tried and failed.")
                sys.exit(1)
            else:
                sleep(0.1)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(infoMain(loop))


main()
