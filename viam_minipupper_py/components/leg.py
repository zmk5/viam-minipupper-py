"""Minipupper Leg Viam Component."""
import asyncio
from typing import Any
from typing import Dict
from typing import Optional

from viam.components.arm import Arm
from viam.operations import run_with_operation
from viam.proto.common import Pose
from viam.proto.common import WorldState
from viam.proto.component.arm import JointPositions

from MangDang.mini_pupper.Config import PWMParams
from MangDang.mini_pupper.Config import ServoParams
from MangDang.mini_pupper.HardwareInterface import send_servo_command


class PupperLeg(Arm):
    """Mini Pupper Viam subclassed component."""

    def __init__(self, name: str, leg_idx: int):
        self.pwm_params = PWMParams()
        self.servo_params = ServoParams()
        self.leg_idx = leg_idx

        # Starting joint positions
        self.joint_positions = JointPositions(values=[0, 0, 0, 0, 0, 0])
        self.is_stopped = True
        super().__init__(name)

    async def get_end_position(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Pose:
        """
        Get the current position of the end of the arm expressed as a Pose.

        Returns: The location and orientation of the arm described as a Pose.
        """
        ...

    async def move_to_position(
        self,
        pose: Pose,
        world_state: Optional[WorldState] = None,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ):
        """
        Move the end of the arm to the Pose specified in ``pose``.
        When obstacles are specified in ``world_state``, the motion plan of the arm will avoid them.

        Args:

            pose (Pose): The destination Pose for the arm.

            world_state (WorldState): The obstacles for the arm to avoid on its way to ``pose``.
        """

    async def get_joint_positions(
        self, extra: Optional[Dict[str, Any]] = None, **kwargs
    ) -> JointPositions:
        return self.joint_positions

    @run_with_operation
    async def move_to_joint_positions(
        self,
        positions: JointPositions,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        print("IN LEG HERE 0")
        operation = self.get_operation(kwargs)

        self.is_stopped = False
        self.joint_positions = positions
        print("IN LEG HERE 1")
        for axis_idx in range(3):
            send_servo_command(
                self.pwm_params,
                self.servo_params,
                # self.joint_positions.values[0:3]
                self.joint_positions.values[axis_idx],
                axis_idx,
                self.leg_idx,
            )
        print("IN LEG HERE 2")
        if await operation.is_cancelled():
            await self.stop()
        print("IN LEG HERE 3")
        self.is_stopped = True

    async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self.is_stopped = True
