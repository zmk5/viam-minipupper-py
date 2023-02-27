"""Minipupper Joystick Controller Viam Component."""
import asyncio
import functools

import numpy as np

from viam.components.base import Base
from viam.components.input import Control
from viam.components.input import Controller
from viam.components.input import Event
from viam.components.input import EventType
from viam.proto.common import Vector3

from MangDang.mini_pupper.Config import Configuration

from viam_minipupper_py.pupper.joystick import Command
from viam_minipupper_py.pupper.joystick import Toggles
from viam_minipupper_py.pupper.state import State
from viam_minipupper_py.pupper.utils import deadband
from viam_minipupper_py.pupper.utils import clipped_first_order_filter


class Joystick:

    def __init__(self):
        self.command = Command()
        self.config = Configuration()
        self.previous = Toggles()
        self.saved = {
            "x": 0.0,
            "y": 0.0,
            "yaw": 0.0,
            "pitch": 0.0,
            "height": 0.0,
        }

    def toggle_gait(self, event: Event):
        if event.value == 1 and self.previous.gait_toggle == 0:
            self.command.trot_event = 1
        else:
            self.command.trot_event = 0

        self.previous.gait_toggle = self.command.trot_event

    def toggle_hop(self, event: Event):
        if event.value == 1 and self.previous.hop_toggle == 0:
            self.command.hop_event = 1
        else:
            self.command.hop_event = 0

        self.previous.hop_toggle = self.command.hop_event

    def toggle_dance_switch(self, event: Event):
        if event.value == 1 and self.previous.dance_swith_toggle != 1:
            self.command.dance_switch_event = 1
        else:
            self.command.dance_switch_event = 0

        self.previous.dance_swith_toggle = self.command.dance_switch_event

    def toggle_gait_switch(self, event: Event):
        print("HERE")
        if event.value == 1 and self.previous.gait_switch_toggle == 0:
            self.command.gait_switch_event = 1
        else:
            self.command.gait_switch_event = 0

        self.previous.gait_switch_toggle = self.command.gait_switch_event

    def toggle_dance(self, event: Event):
        if event.value == 1 and self.previous.dance_activate_toggle == 0:
            self.command.dance_activate_event = 1
        else:
            self.command.dance_activate_event = 0

        self.previous.dance_activate_toggle = self.command.dance_activate_event

    def toggle_activate(self, event: Event):
        if event.value == 1 and self.previous.activate_toggle == 0:
            print("ACTIVATING --------------")
            self.command.activate_event = 1
        else:
            print("DEACTIVATING ------------")
            self.command.activate_event = 0

        self.previous.activate_toggle = self.command.activate_event

    def toggle_shutdown(self, event: Event):
        self.command.shutdown_signal = event.value

    def change_x(self, event: Event):
        self.saved["x"] = event.value

    def change_y(self, event: Event):
        self.saved["y"] = event.value

    def change_roll(self, event: Event):
        self.saved["roll"] = -1 * event.value

    def change_pitch(self, event: Event):
        self.saved["pitch"] = event.value

    def change_yaw(self, event: Event):
        self.saved["yaw"] = event.value

    def change_height(self, event: Event):
        self.saved["height"] = event.value

    async def handleController(self, controller: Controller):
        resp = await controller.get_events()
        # Show the input controller's buttons/axes
        # print(f"Controls: {resp}")

        if Control.BUTTON_RT in resp:
            controller.register_control_callback(
                Control.BUTTON_RT,
                [EventType.BUTTON_PRESS, EventType.BUTTON_RELEASE],
                # functools.partial(self.toggle_gait, self),
                self.toggle_gait,
            )

        if Control.BUTTON_RT2 in resp:
            controller.register_control_callback(
                Control.BUTTON_RT2,
                [EventType.BUTTON_PRESS, EventType.BUTTON_RELEASE],
                # functools.partial(self.toggle_gait_switch, self),
                self.toggle_gait_switch,
            )

        if Control.BUTTON_LT in resp:
            controller.register_control_callback(
                Control.BUTTON_LT,
                [EventType.BUTTON_PRESS],
                # functools.partial(self.toggle_activate, self),
                self.toggle_activate,
            )

        if Control.BUTTON_LT2 in resp:
            controller.register_control_callback(
                Control.BUTTON_LT2,
                [EventType.BUTTON_PRESS],
                # functools.partial(self.toggle_dance_switch, self),
                self.toggle_dance_switch,
            )

        if Control.BUTTON_NORTH in resp:
            controller.register_control_callback(
                Control.BUTTON_NORTH,
                [EventType.BUTTON_PRESS],
                # functools.partial(self.toggle_shutdown, self),
                self.toggle_shutdown,
            )

        if Control.BUTTON_EAST in resp:
            controller.register_control_callback(
                Control.BUTTON_EAST,
                [EventType.BUTTON_PRESS],
                # functools.partial(self.toggle_dance, self),
                self.toggle_dance,
            )

        if Control.ABSOLUTE_X in resp:
            controller.register_control_callback(
                Control.ABSOLUTE_X,
                [EventType.POSITION_CHANGE_ABSOLUTE],
                # functools.partial(self.change_x, self),
                self.change_x,
            )

        if Control.ABSOLUTE_Y in resp:
            controller.register_control_callback(
                Control.ABSOLUTE_Y,
                [EventType.POSITION_CHANGE_ABSOLUTE],
                # functools.partial(self.change_y, self),
                self.change_y,
            )

        if Control.ABSOLUTE_RX in resp:
            controller.register_control_callback(
                Control.ABSOLUTE_X,
                [EventType.POSITION_CHANGE_ABSOLUTE],
                # functools.partial(self.change_yaw, self),
                self.change_yaw,
            )

        if Control.ABSOLUTE_RY in resp:
            controller.register_control_callback(
                Control.ABSOLUTE_Y,
                [EventType.POSITION_CHANGE_ABSOLUTE],
                # functools.partial(self.change_pitch, self),
                self.change_pitch
            )

        # TODO: No D-Pad buttons for roll and height

        # while True:
        #     await asyncio.sleep(0.01)
            # global cmd
            # if "y" in cmd:
            #     respon = await modal.set_power(linear=Vector3(x=0,y=cmd["y"],z=0), angular=Vector3(x=0,y=0,z=turn_amt))
            #     cmd = {}
            #     print(respon)

    def get_command(self, state: State, dt: float = 0.1) -> Command:
        """Get command based on inputs from device."""
        self.command.horizontal_velocity = np.array([
            self.saved["y"] * self.config.max_x_velocity,
            self.saved["x"] * -self.config.max_y_velocity,
        ])
        self.command.yaw_rate = self.saved["yaw"] * -self.config.max_yaw_rate

        pitch = self.saved["pitch"] * self.config.max_pitch
        deadbanded_pitch = deadband(pitch, self.config.pitch_deadband)
        pitch_rate = clipped_first_order_filter(
            state.pitch,
            deadbanded_pitch,
            self.config.max_pitch_rate,
            self.config.pitch_time_constant,
        )
        self.command.pitch = state.pitch + dt * pitch_rate

        # self.command.height = (
        #     state.height - dt * self.config.z_speed * self.saved["height"]
        # )

        # self.command.roll = (
        #     state.roll + dt * self.config.roll_speed * self.saved["roll"]
        # )

        return self.command
