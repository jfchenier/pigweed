#!/usr/bin/env python
# Copyright 2020 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Simple example script that uses pw_rpc."""

import argparse
import os
from pathlib import Path

import serial  # type: ignore

from pw_hdlc.rpc import HdlcRpcClient, default_channels

# Point the script to the .proto file with our RPC services.
PROTO = Path(os.environ['PW_ROOT'], 'pw_rpc/echo.proto')

def on_next(call_object, response):
    pass

def on_completed(call_object, status):
    pass

def script(device: str, baud: int) -> None:
    # Set up a pw_rpc client that uses HDLC.
    ser = serial.Serial(device, baud, timeout=0.01)
    client = HdlcRpcClient(
        lambda: ser.read(4096), [PROTO], default_channels(ser.write)
    )

    # Make a shortcut to the EchoService.
    echo_service = client.rpcs().pw.rpc.ByteService

    iteration = 10000000

    rpc = echo_service.Receive
    #use input status to tell the server how many itertation we want to receive on the stream.
    input_status = iteration

    call = rpc.invoke(rpc.request(status=input_status), on_next, on_completed)
    responses = call.get_responses()

    call.wait()

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--device', '-d', default='/dev/ttyACM0', help='serial device to use'
    )
    parser.add_argument(
        '--baud',
        '-b',
        type=int,
        default=115200,
        help='baud rate for the serial device',
    )
    script(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
