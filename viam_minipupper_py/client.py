#!/usr/bin/env python3
import asyncio
from multiprocessing import Process
import multiprocessing
import os
import sys
import threading
import time

import numpy as np

from PIL import Image

sys.path.append("/home/ubuntu/Robotics/QuadrupedRobot")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("/home/ubuntu/Robotics/QuadrupedRobot") for name in dirs])

from MangDang.LCD.ST7789 import ST7789
from MangDang.LCD.gif import AnimatedGif
from MangDang.mini_pupper.HardwareInterface import HardwareInterface
from MangDang.mini_pupper.Config import Configuration

from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions

from viam_minipupper_py.pupper.control.controller import Controller
from viam_minipupper_py.pupper.joystick import JoystickInterface
from viam_minipupper_py.pupper.kinematics import four_legs_inverse_kinematics
from viam_minipupper_py.pupper.movement import MovementScheme
from viam_minipupper_py.pupper.state import State


async def client():
    """Connect to robot and initiate client."""
    opts = RobotClient.Options(dial_options=DialOptions(insecure=True))
    async with await RobotClient.at_address("localhost:9090", opts) as robot:
        pass


def main():
    """Run the minipupper robot."""
    print("Starting Client...")
    asyncio.run(client())


if __name__ == "__main__":
    main()
