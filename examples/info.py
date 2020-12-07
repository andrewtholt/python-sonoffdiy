#!/usr/bin/env python3
# pylint: disable=W0621
"""Asynchronous Python client for Sonoff DIY device."""

import asyncio

from sonoffdiy import SonoffDIY


async def infoMain(loop):
    tryAgain = True
    count = 4

    while tryAgain:
        try:
            async with SonoffDIY("192.168.10.169", device_id="1000c8c4b5", loop=loop) as diy:
                info = await diy.update_info()
                print(info)
            tryAgain = False
        except:
            count -=1
            tryAgain = True
            if count < 0:
                print("Tried and failed.")




def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(infoMain(loop))

main()
