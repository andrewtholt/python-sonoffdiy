#!/usr/bin/env python3
# pylint: disable=W0621
"""Asynchronous Python client for Sonoff DIY device."""

import asyncio

from sonoffdiy import SonoffDIY


async def main(loop):
    """Show example on controlling your Sonoff DIY device."""
    async with SonoffDIY("192.168.10.169", device_id="1000c8c4b5", loop=loop) as diy:
        info = await diy.update_info()
        print(info)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
