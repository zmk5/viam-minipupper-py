#!/usr/bin/env python3
"""Minipupper server function."""
import asyncio
import logging
import sys

from viam.rpc.server import Server

# from viam.components.camera import Camera
# from viam.components.sensor import Sensor
from viam.components.input import Controller

# from viam.components.pose_tracker import PoseTracker

from viam_minipupper_py.components.leg import PupperLeg


async def run(host: str, port: int, log_level: int):
    """Run MiniPupper component server."""
    front_right_leg = PupperLeg("frl", 0)
    front_left_leg = PupperLeg("fll", 1)
    hind_right_leg = PupperLeg("hrl", 2)
    hind_left_leg = PupperLeg("hll", 3)

    server = Server(
        components=[
            front_right_leg,
            front_left_leg,
            hind_right_leg,
            hind_left_leg,
            # joystick,
        ]
    )
    await server.serve(host=host, port=port, log_level=log_level)
    # await server.serve()


def main():
    host = "localhost"
    port = 9090
    # port = 8080
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
