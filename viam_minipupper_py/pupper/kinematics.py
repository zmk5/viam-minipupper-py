from typing import List
from typing import Union

import numpy as np

from MangDang.mini_pupper.Config import Configuration


def leg_explicit_inverse_kinematics(
    r_body_foot: np.ndarray, leg_index: int, config: Configuration
) -> np.ndarray:
    """Find the joint angles corresponding to the given body-relative foot
    position for a given leg and configuration

    Parameters
    ----------
    r_body_foot : np.ndarray
        [description]
    leg_index : int
        [description]
    config : Configuration
        [description]

    Returns
    -------
    numpy array (3)
        Array of corresponding joint angles.
    """
    (x, y, z) = r_body_foot

    # Distance from the leg origin to the foot, projected into the y-z plane
    R_body_foot_yz = np.power(np.square(y) + np.square(z), 0.5)

    # Distance from the leg's forward/back point of rotation to the foot
    R_hip_foot_yz = np.power(
        np.square(R_body_foot_yz) - np.square(config.ABDUCTION_OFFSET), 0.5
    )

    # Interior angle of the right triangle formed in the y-z plane by the leg that is coincident to the ab/adduction axis
    # For feet 2 (front left) and 4 (back left), the abduction offset is positive, for the right feet, the abduction offset is negative.
    arccos_argument = config.ABDUCTION_OFFSETS[leg_index] / R_body_foot_yz
    arccos_argument = np.clip(arccos_argument, -0.99, 0.99)
    phi = np.arccos(arccos_argument)

    # Angle of the y-z projection of the hip-to-foot vector, relative to the positive y-axis
    hip_foot_angle = np.arctan2(z, y)

    # Ab/adduction angle, relative to the positive y-axis
    abduction_angle = phi + hip_foot_angle

    # theta: Angle between the tilted negative z-axis and the hip-to-foot vector
    theta = np.arctan2(-x, R_hip_foot_yz)

    # Distance between the hip and foot
    R_hip_foot = np.power(np.square(R_hip_foot_yz) + np.square(x), 0.5)

    # Angle between the line going from hip to foot and the link L1
    arccos_argument = (
        np.square(config.LEG_L1) + np.square(R_hip_foot) - np.square(config.LEG_L2)
    ) / (2 * config.LEG_L1 * R_hip_foot)
    arccos_argument = np.clip(arccos_argument, -0.99, 0.99)
    trident = np.arccos(arccos_argument)

    # Angle of the first link relative to the tilted negative z axis
    hip_angle = theta + trident

    # Angle between the leg links L1 and L2
    arccos_argument = (
        np.square(config.LEG_L1) + np.square(config.LEG_L2) - np.square(R_hip_foot)
    ) / (2 * config.LEG_L1 * config.LEG_L2)
    arccos_argument = np.clip(arccos_argument, -0.99, 0.99)
    beta = np.arccos(arccos_argument)

    # Angle of the second link relative to the tilted negative z axis
    knee_angle = hip_angle - (np.pi - beta)

    return np.array([abduction_angle, hip_angle, knee_angle])


def four_legs_inverse_kinematics(
    r_body_foot: np.ndarray, config: Configuration
) -> np.ndarray:
    """Find the joint angles for all twelve DOF correspoinding to the given
    matrix of body-relative foot positions.

    Parameters
    ----------
    r_body_foot : np.ndarray (3,4)
        Matrix of the body-frame foot positions. Each column corresponds to
        a separate foot.
    config : Config object
        Object of robot configuration parameters.

    Returns
    -------
    np.ndarray (3,4)
        Matrix of corresponding joint angles.
    """
    alpha = np.zeros((3, 4))
    for i in range(4):
        body_offset = config.LEG_ORIGINS[:, i]
        alpha[:, i] = leg_explicit_inverse_kinematics(
            r_body_foot[:, i] - body_offset, i, config
        )
    return alpha
