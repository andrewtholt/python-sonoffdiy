#!/usr/bin/env python3
# pylint: disable=W0621
"""Asynchronous Python client for Sonoff DIY device."""

import asyncio

from sonoffdiy import SonoffDIY


async def main(loop):
    tryAgain = True
    count = 3

    """Show example on controlling your Sonoff DIY device."""
    while tryAgain == True:
        print("Count=",count)
        try:
            async with SonoffDIY("192.168.10.169", device_id="1000c8c4b5", loop=loop) as diy:
                info = await diy.update_info()
                print(info)
        
                if not info.on:
                    await diy.turn_on()
                else:
                    await diy.turn_off()

                tryAgain = False
        except:
            print("Something broke")
            count -= 1
            tryAgain = True

            if count == 0:
                print("Tried and failed.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
