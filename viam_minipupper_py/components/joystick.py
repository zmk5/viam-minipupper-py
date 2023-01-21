"""Minipupper Joystick Controller Viam Component."""
import asyncio
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import numpy as np

from viam.components.input import Control
from viam.components.input import Controller
from viam.components.input import ControlFunction
from viam.components.input import Event
from viam.components.input import EventType


@dataclass
class Command:
    """Store movement commands."""
    horizontal_velocity: np.ndarray = np.array([0, 0])
    yaw_rate: float = 0.0
    height: float = -0.07
    pitch: float = 0.0
    roll: float = 0.0
    activation: int = 0

    hop_event: bool = False
    trot_event: bool = False
    activate_event: bool = False
    dance_activate_event: bool = False
    dance_switch_event: bool = False
    gait_switch_event: bool = False
    shutdown_signal: bool = False


class PupperJoystickController(Controller):
    """PS3 Joystick Controller component for Minipupper."""

    def __init__(self, name: str):
        super().__init__(name)
        self.horizontal_velocity = np.array([0, 0])


    async def get_controls(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> List[Control]:
        """
        Returns a list of Controls provided by the Controller

        Returns:
            List[Control]: List of controls provided by the Controller
        """

    async def get_events(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Dict[Control, Event]:
        """
        Returns the most recent Event for each input
        (which should be the current state)

        Returns:
            Dict[Control, Event]: The most recent event for each input
        """

    def register_control_callback(
        self,
        control: Control,
        triggers: List[EventType],
        function: Optional[ControlFunction],
        *,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Register a function that will fire on given EventTypes for a given
        Control

        Args:
            control (Control): The control to register the function for
            triggers (List[EventType]): The events that will
                trigger the function
            function (ControlFunction): The function to run on
                specific triggers
        """


    async def trigger_event(self, event: Event, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        """Directly send an Event (such as a button press) from external code

        Args:
            event (Event): The event to trigger
        """

