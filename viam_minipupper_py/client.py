#!/usr/bin/env python3
import asyncio

from viam.components.arm import Arm
from viam.components.arm import Pose
from viam.components.base import Base
from viam.components.base import Vector3
from viam.components.camera import Camera
from viam.components.motor import Motor
from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions


async def client():
    opts = RobotClient.Options(dial_options=DialOptions(insecure=True))
    async with await RobotClient.at_address("localhost:9090", opts) as robot:

        print("\n#### RESOURCES ####")
        print(f"Resources: {robot.resource_names}")

        print("\n#### STATUS ####")
        print(f"Robot status response received: {await robot.get_status()}")

        print("\n#### ARM ####")
        # arm = Arm.from_robot(robot, 'arm0')
        # await arm.move_to_position(Pose(x=0, y=1, z=2, o_x=3, o_y=4, o_z=5, theta=6))
        # position = await arm.get_end_position()
        # print(f'Arm position is: {position}')

        print("\n#### BASE ####")
        # base = Base.from_robot(robot, 'base0')
        # await base.set_velocity(Vector3(x=0, y=1, z=2), Vector3(x=3, y=4, z=5))
        # await base.stop()

        print("\n#### CAMERA ####")
        # camera = Camera.from_robot(robot, 'camera0')
        # img = await camera.get_frame()
        # img.show()
        # await asyncio.sleep(1)
        # img.close()

        print("\n#### MOTOR ####")
        # motor = Motor.from_robot(robot, 'motor0')
        # await motor.go_for(rpm=100, revolutions=10)
        # await motor.stop()


def main():
    print("Starting Client...")
    asyncio.run(client())


if __name__ == "__main__":
    main()
