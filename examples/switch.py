#!/usr/bin/env python3
# pylint: disable=W0621
"""Asynchronous Python client for Sonoff DIY device."""

import asyncio
import getopt
import sys
from sonoffdiy import SonoffDIY

def usage():
    print("Usage: switch.py -h|--help -v|--verbose -c <cfg file>| --config=<cfg file> -o <out|off> | --output=<on|off>" )

async def switchMain(loop,state):
    tryAgain = True
    count = 4

#    print(state)

    """Show example on controlling your Sonoff DIY device."""
    while tryAgain == True:
#        print("Count=",count)
        try:
            async with SonoffDIY("192.168.10.169", device_id="1000c8c4b5", loop=loop) as diy:
                info = await diy.update_info()
#                print(info)
        
#                if not info.on:
                if state == 'on':
                    await diy.turn_on()
                else:
                    await diy.turn_off()

                tryAgain = False
        except:
#            print("Something broke")
            count -= 1
            tryAgain = True

            if count < 0:
                print("Tried and failed.")


def main():

    configFile = "/etc/HomeAutomation/config.json"
    name = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:ho:vn:", ["config=","help", "out=","name="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    verbose = False
    state = "error"

    for o, a in opts:
        if o in ("-v","--verbose"):
            verbose = True
        elif o in ("-c", "--config"):
            configFile = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--out"):
            state = a
        elif o in ("-n", "--name"):
            name = a

    if verbose:
        print("Outlet name     :" + name )
        print("Requested state :" + state )

    if  state == "on":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(switchMain(loop,state))
    elif state == "off":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(switchMain(loop,state))
    else:
        print("Invalid state ", state)

        sys.exit(3)

main()

