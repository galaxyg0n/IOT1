#!/usr/bin/env python3

'''
                    ___           ___           ___
        ___        /\__\         /\  \         /\  \
       /\  \      /::|  |       /::\  \       /::\  \
       \:\  \    /:|:|  |      /:/\:\  \     /:/\ \  \
       /::\__\  /:/|:|  |__   /::\~\:\  \   _\:\~\ \  \
    __/:/\/__/ /:/ |:| /\__\ /:/\:\ \:\__\ /\ \:\ \ \__\
   /\/:/  /    \/__|:|/:/  / \:\~\:\ \/__/ \:\ \:\ \/__/
   \::/__/         |:/:/  /   \:\ \:\__\    \:\ \:\__\
    \:\__\         |::/  /     \:\ \/__/     \:\/:/  /
     \/__/         /:/  /       \:\__\        \::/  /
                   \/__/         \/__/         \/__/


    File:          coapthing.py


    Purpose:       Exemplarily implementation
                   of a "thing" that uses
                   the CoAP protocol to
                   interact with other devices.

                   This is the main file and
                   program entry point.

                   The pins of connected
                   hardware to the GrovePi
                   board should be declared
                   here as well as the
                   resources (sensors and
                   actuators) this device/
                   "thing" should provide.


    Remarks:       - python3 is required due
                     to the asyncio and aiocoap
                     libraries.
                     The aiocoap library makes
                     use of coroutines.


    Author:        P. Leibundgut <leiu@zhaw.ch>


    Date:          09/2023

'''

import logging

import asyncio

import aiocoap
import aiocoap.resource as resource

import log

from Actuator import Actuator

from ButtonResource import ButtonResource
from LedResource import LedResource
from TimeResource import TimeResource


# connected hardware
LED0_PIN    = int( 4 )
BUTTON0_PIN = int( 3 )

GENERAL_AIOCOAP_LOGGER_NAME = "coap-server"

# logging setup
logger = log.setup_custom_logger( GENERAL_AIOCOAP_LOGGER_NAME )

# CoAP server resources
resources = { }


async def run_srvr():
  loop = None

  # Resource tree creation
  root = resource.Site()

  await aiocoap.Context.create_server_context( root )
  loop = asyncio.get_event_loop()

  root.add_resource(
    ( '.well-known', 'core'    ), \
    resource.WKCResource( root.get_resources_as_linkheader )
  )

  resources[ 'button0' ] = \
    ButtonResource(
        connector = BUTTON0_PIN,
        loop = loop, logger = logger,
        polling_interval = float( 0.2 ),
        sampling_resolution = int( 2 ),
        actuator_uris = [ "coap://localhost:5683/actuators/led0" ]
    )

  resources[ 'led0' ] = \
    LedResource( connector = LED0_PIN,
                 logger = logger,
                 nuances_resolution = int( 2 )
    )

  resources[ 'clock0' ]  = TimeResource( logger = logger )

  root.add_resource( ( 'sensors',   'button0' ), resources[ 'button0' ] )
  root.add_resource( ( 'actuators', 'led0'    ), resources[ 'led0' ] )
  root.add_resource( ( 'stuff',     'clock0'  ), resources[ 'clock0' ] )

  # Run forever ...
  await asyncio.get_running_loop().create_future()


def main():
  try:
    asyncio.run( run_srvr() )
  except KeyboardInterrupt:
    # clean up actuators.
    # set their output to low
    for key, value in resources.items():
      if isinstance( value, Actuator ):
        value.__exit__( None, None, None )
    logger.debug( "\n\n\n\n\n" + \
                  "+--------------------------------------------------------------------+\n" + \
                  "| Thing was interrupted by key stroke. Thats all, folks! Exiting ... |\n" + \
                  "+--------------------------------------------------------------------+" )


if __name__ == "__main__":
  main()

