#!/usr/bin/env python3
# pylint: disable=W0621
"""Asynchronous Python client for Sonoff DIY device."""

import asyncio
import getopt
import json
import os.path
import sys

from sonoffdiy import SonoffDIY


def usage():
    print( "Usage: switch.py -h|--help -v|--verbose  -n <name> | --name=<name> -c <cfg file>| --config=<cfg file> -o <out|off> | --output=<on|off>")
    print("")
    print("\t-h|-help\t\tThis.")    
    print("\t-v|--verbose\t\tVerbose.") 
    print("\t-n <name>|--name=<name>\tName of the device to control.")
    print("\t-c <cfg>|--config=<cfg>\tLoad this config file.")
    print("\t-o <on|off>|--out=<on|off>\tSet the device to this state.")

async def switchMain(loop, ip, deviceID, state):
    tryAgain = True
    count = 4

    """Show example on controlling your Sonoff DIY device."""
    while tryAgain:
        try:
            #            async with SonoffDIY("192.168.10.169", device_id="1000c8c4b5", loop=loop) as diy:
            async with SonoffDIY(ip, device_id=deviceID, loop=loop) as diy:
                info = await diy.update_info()

                if state == "on":
                    await diy.turn_on()
                else:
                    await diy.turn_off()

                tryAgain = False
        except:
            count -= 1
            tryAgain = True

            if count < 0:
                print("Tried and failed.")


def main():

    configFile = "/etc/HomeAutomation/config.json"
    name = ""
    test = False

    try:
        opts, args = getopt.getopt( sys.argv[1:], "c:ho:vn:t", ["config=", "help", "out=", "name=", "test"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    verbose = False
    state = "error"

    for o, a in opts:
        if o in ("-v", "--verbose"):
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
        elif o in ("-t", "--test"):
            test = True
            verbose = True

    if verbose:
        print("Outlet name     :" + name)
        print("Requested state :" + state)

        if test:
            print("Test")

    if not os.path.isfile(configFile):
        print("Config file " + configFile + " does not exist")
        sys.exit(1)

    with open(configFile) as cf:
        config = json.load(cf)
        print(config["SonoffDIY"])

        sonoff = config["SonoffDIY"]

        if sonoff.get(name):
            print("Name :" + name)
            ip = sonoff["test"]["ip"]
            deviceID = sonoff["test"]["device_id"]

            print("\tIP        :" + ip)
            print("\tDevice ID :" + deviceID)
        else:
            print(name + " not found")

    valid = False
    if not test:
        if state in ("on", "off"):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(switchMain(loop, ip, deviceID, state))
        else:
            print("Invalid state ", state)
            sys.exit(3)


main()
