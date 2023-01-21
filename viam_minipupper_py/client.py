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

from rich import print

from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions

sys.path.append("/home/ubuntu/QuadrupedRobot")
sys.path.extend(
    [
        os.path.join(root, name)
        for root, dirs, _ in os.walk("/home/ubuntu/QuadrupedRobot")
        for name in dirs
    ]
)

from viam.proto.component.arm import JointPositions

# from MangDang.LCD.ST7789 import ST7789
# from MangDang.LCD.gif import AnimatedGif
from MangDang.mini_pupper.HardwareInterface import HardwareInterface
from MangDang.mini_pupper.Config import Configuration

from viam_minipupper_py.components.leg import PupperLeg
from viam_minipupper_py.pupper.control.controller import Controller
from viam_minipupper_py.pupper.joystick import JoystickInterface
from viam_minipupper_py.pupper.kinematics import four_legs_inverse_kinematics
from viam_minipupper_py.pupper.movement import MovementScheme
from viam_minipupper_py.pupper.state import State


QUAT_ORIENTATION = np.array([1, 0, 0, 0])

# TODO: Consider removing
CARTOONS_FOLDER = "/home/ubuntu/QuadrupedRobot/Mangdang/LCD/cartoons/"
CURRENT_SHOW = ""

# with open("/home/ubuntu/.hw_version", "r") as hw_f:
#     HW_VERSION = hw_f.readline()
#     DISP = ST7789(14, 15, 17) if HW_VERSION == "P1\n" else ST7789(27, 24, 26)


# def pic_show(disp, pic_name, _lock):
#     """Show the specify picture
#     Parameter:
#         disp : display instance
#         pic_name : picture name to show
#     Return : None
#     """
#     if pic_name == "":
#         return

#     global CURRENT_SHOW
#     if pic_name == CURRENT_SHOW:
#         return

#     image = Image.open(CARTOONS_FOLDER + pic_name)
#     image.resize((320, 240))
#     _lock.acquire()
#     disp.display(image)
#     _lock.release()
#     CURRENT_SHOW = pic_name


# def animated_thr_fun(_disp, duration, is_connect, current_leg, _lock):
#     """
#     The thread funcation to show sleep animated gif
#     Parameter: None
#     Returen: None
#     """
#     try:
#         gif_player = AnimatedGif(_disp, width=320, height=240, folder=CARTOONS_FOLDER)
#         last_time = time.time()
#         last_joint_angles = np.zeros(3)
#         while True:
#             if is_connect.value == 1:
#                 # if ((current_leg[0]==last_joint_angles[0]) and  (current_leg[1]==last_joint_angles[1]) and (current_leg[2]==last_joint_angles[2])) == False :
#                 if (
#                     (current_leg[0] == last_joint_angles[0])
#                     and (current_leg[1] == last_joint_angles[1])
#                 ) is False:
#                     last_time = time.time()
#                     last_joint_angles[0] = current_leg[0]
#                     last_joint_angles[1] = current_leg[1]
#                     # last_joint_angles[2] = current_leg[2]
#                 if (time.time() - last_time) > duration:
#                     _lock.acquire()
#                     gif_player.play()
#                     _lock.release()
#                     time.sleep(0.5)
#             else:
#                 last_time = time.time()
#                 time.sleep(1.5)
#     except KeyboardInterrupt:
#         _lock.release()
#         pass


def cmd_dump(cmd: State):
    """Dump all info about PS4 command (DEBUG)."""
    print("\nGet PS4 command:")
    print(f"\thorizontal_velocity: {cmd.horizontal_velocity}")
    print(f"\tyaw_rate: {cmd.yaw_rate}")
    print(f"\theight: {cmd.height}")
    print(f"\tpitch: {cmd.pitch}")
    print(f"\troll: {cmd.roll}")
    print(f"\tactivation: {cmd.activation}")
    print(f"\thop_event: {cmd.hop_event}")
    print(f"\ttrot_event: {cmd.trot_event}")
    print(f"\tactivate_event {cmd.activate_event}")


async def client():
    """Connect to robot and initiate client."""
    opts = RobotClient.Options(dial_options=DialOptions(insecure=True))
    async with await RobotClient.at_address("localhost:9090", opts) as robot:
        # Create empty configuration
        config = Configuration()
        hardware_interface = HardwareInterface()

        legs = {
            0: PupperLeg.from_robot(robot, "frl"),
            1: PupperLeg.from_robot(robot, "fll"),
            2: PupperLeg.from_robot(robot, "hrl"),
            3: PupperLeg.from_robot(robot, "hll"),
        }

        # show logo
        # global DISP
        # DISP.begin()
        # DISP.clear()
        # image = Image.open(CARTOONS_FOLDER + "logo.png")
        # image.resize((320, 240))
        # DISP.display(image)

        shutdown_counter = 0  # counter for shuudown cmd

        # Start animated process
        # duration = 10
        is_connect = multiprocessing.Value("l", 0)
        # current_leg = multiprocessing.Array("d", [0, 0, 0])
        # lock = multiprocessing.Lock()
        # animated_process = Process(
        #     target=animated_thr_fun,
        #     args=(DISP, duration, is_connect, current_leg, lock),
        # )
        # animated_process.start()

        # Create movement group scheme
        MovementLib = []
        movement_ctl = MovementScheme(MovementLib)

        # Create controller and user input handles
        controller = Controller(
            config,
            four_legs_inverse_kinematics,
        )
        state = State()
        print("Creating joystick listener...")
        joystick_interface = JoystickInterface(config)
        print("Done.")

        last_loop = time.time()

        print("Summary of gait parameters:")
        print("overlap time: ", config.overlap_time)
        print("swing time: ", config.swing_time)
        print("z clearance: ", config.z_clearance)
        print("x shift: ", config.x_shift)

        # Wait until the activate button has been pressed
        while True:
            print("Waiting for L1 to activate robot.")
            while True:
                command = joystick_interface.get_command(state)
                joystick_interface.set_color(config.ps4_deactivated_color)
                if command.activate_event == 1:
                    break
                time.sleep(0.1)
            print("Robot activated.")
            is_connect.value = 1
            joystick_interface.set_color(config.ps4_color)
            # pic_show(DISP, "walk.png", lock)

            while True:
                now = time.time()
                if now - last_loop < config.dt:
                    continue
                last_loop = time.time()

                # Parse the udp joystick commands and then update the robot controller's parameters
                command = joystick_interface.get_command(state)
                # cmd_dump(command)
                # _pic = "walk.png" if command.yaw_rate == 0 else "turnaround.png"
                # if command.trot_event == True:
                #     _pic = "walk_r1.png"
                # pic_show(DISP, _pic, lock)
                if command.activate_event == 1:
                    is_connect.value = 0
                    # pic_show(DISP, "notconnect.png", lock)
                    print("Deactivating Robot")
                    break
                state.quat_orientation = QUAT_ORIENTATION
                # movement scheme
                movement_switch = command.dance_switch_event
                gait_state = command.trot_event
                dance_state = command.dance_activate_event
                shutdown_signal = command.shutdown_signal

                # shutdown counter
                if shutdown_signal is True:
                    shutdown_counter = shutdown_counter + 1
                    # press shut dow button more 3s(0.015*200), shut down system
                    if shutdown_counter >= 200:
                        print("shutdown system now")
                        os.system("systemctl stop robot")
                        os.system("shutdown -h now")

                # gait and movement control
                # if triger tort event, reset the movement number to 0
                if (gait_state is True or dance_state is True):
                    movement_ctl.resetMovementNumber()
                movement_ctl.runMovementScheme(movement_switch)
                food_location = movement_ctl.getMovemenLegsLocation()
                attitude_location = movement_ctl.getMovemenAttitude()
                robot_speed = movement_ctl.getMovemenSpeed()
                controller.run(
                    state, command, food_location, attitude_location, robot_speed
                )

                for i in range(4):
                    # Convert state joint angles to joint positions
                    thigh = state.joint_angles[0, i]
                    hip = state.joint_angles[1, i]
                    calf = state.joint_angles[2, i]
                    await legs[i].move_to_joint_positions(
                        JointPositions(values=[thigh, hip, calf, 0, 0, 0])
                    )


                # Update the pwm widths going to the servos
                # hardware_interface.set_actuator_postions(state.joint_angles)
                # current_leg[0] = state.joint_angles[0][0]
                # current_leg[1] = state.joint_angles[1][0]
                # current_leg[2]= state.joint_angles[2][0]


def main():
    """Run the minipupper robot."""
    print("Starting Client...")
    asyncio.run(client())


if __name__ == "__main__":
    main()
