#!/usr/bin/env python3
# pylint: disable=W0621
"""Asynchronous Python client for Sonoff DIY device."""

import asyncio
import json
import sys
from time import sleep

import getopt
import os.path

from sonoffdiy import SonoffDIY

def usage():    
    print("Usage: info.py -h|--help -v|--verbose -n <name> | --name=<name> -c <cfg file>| --config=<cfg file>")
    print("")
    print("\t-h|-help\t\tThis.")
    print("\t-v|--verbose\t\tVerbose.")
    print("\t-n <name>|--name=<name>\tName of the device to interogate.")
    print("\t-c <cfg>|--config=<cfg>\tLoad this config file.")
    
def readConfig(fname):
    if not os.path.isfile(fname):    
        print("Config file " + fname + " does not exist")    
        sys.exit(1)

    with open(fname) as cf:    
        config = json.load(cf)    
    
        sonoff = config["SonoffDIY"]    

        return(sonoff)
    

async def infoMain(loop):
    tryAgain = True
    count = 4

    configFile = "/etc/HomeAutomation/config.json"    
    name = ""     
    
    verbose = False

    try:    
        opts, args = getopt.getopt( sys.argv[1:], "c:hvn:", ["config=", "help",  "name="])
    except getopt.GetoptError as err:    
        print(err)    
        usage()       
        sys.exit(2)    
            
    for o, a in opts:    
        if o in ("-v", "--verbose"):    
            verbose = True
        elif o in ("-c", "--config"):
            configFile = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-n", "--name"):
            name = a

    sonoff = readConfig( configFile )

    ip=""
    deviceID=""
    if sonoff.get(name):    
        print("Name :" + name)    
        ip = sonoff["test"]["ip"]    
        deviceID = sonoff["test"]["device_id"]    

        print("\tIP        :" + ip)    
        print("\tDevice ID :" + deviceID)    
    else:    
        print(name + " not found")
        tryAgain = False

    while tryAgain:
        try:
            async with SonoffDIY(
                ip, device_id=deviceID, loop=loop
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
                sleep(0.2)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(infoMain(loop))


main()
