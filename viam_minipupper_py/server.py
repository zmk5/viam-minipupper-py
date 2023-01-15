#!/usr/bin/env python3
"""Minipupper server function."""
import asyncio
import logging
import sys

from viam.rpc.server import Server

from viam.components.camera import Camera
from viam.components.sensor import Sensor
from viam.components.input import Controller
from viam.components.pose_tracker import PoseTracker

from viam_minipupper_py.components.leg import PupperLeg


async def run(host: str, port: int, log_level: int):
    """Run MiniPupper component server."""
    front_right_leg = PupperLeg("frl")
    front_left_leg = PupperLeg("fll")
    hind_right_leg = PupperLeg("hrl")
    hind_left_leg = PupperLeg("hll")
    joystick = Controller("joystick")

    server = Server(
        components=[
            front_right_leg,
            front_left_leg,
            hind_right_leg,
            hind_left_leg,
            joystick,
        ]
    )
    await server.serve(host=host, port=port, log_level=log_level)


def main():
    host = "localhost"
    port = 9090
    log_level = logging.DEBUG
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        level = sys.argv[3]
        if level.lower() == "q" or level.lower() == "quiet":
            log_level = logging.FATAL
    except (IndexError, ValueError):
        pass
    asyncio.run(run(host, port, log_level))


if __name__ == "__main__":
    main()
