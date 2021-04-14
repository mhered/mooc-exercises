from typing import Tuple

import numpy as np

# MH - FEAR


def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    # MH: creates a mask with 1s in left side of image and 0s in right side
    mid_width = int(np.floor(shape[1]/2))
    mid_height = int(np.floor(shape[0]/2))

    res[mid_height:, 0:mid_width] = 1
    return res


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    # MH: creates a mask with 0s in left side of image and 1s in right side
    mid_width = int(np.floor(shape[1]/2))
    mid_height = int(np.floor(shape[0]/2))

    res[mid_height:, mid_width:] = 1
    return res


# MH - BRAKES
def get_brake_matrix(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    # MH: creates a mask with 1s in lower area
    # This activates when a duckie is close and brakes
    two_thrds_height = int(np.floor(2*shape[0]/3))

    res[two_thrds_height:, :] = 1
    return res


"""
# Alternative #1: EXPLORER
# Notes:requires negative GAIN, not succesful, removed

def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")
    # MH: creates a mask with 1s in the 2/3 lower 1/2 right side corner of the image and 0s elsewhere
    mid_width = int(np.floor(shape[1]/2))
    thrd_height = int(np.floor(shape[0]/3))

    res[thrd_height:, mid_width:] = 1
    return res


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")  # write your function instead of this one
    # MH: creates a mask with 1s in the 2/3 lower 1/2 left side corner of the image and 0s elsewhere
    mid_width = int(np.floor(shape[1]/2))
    thrd_height = int(np.floor(shape[0]/3))

    res[thrd_height:, :mid_width] = 1
    return res
"""
"""
# Alternative #2: WEIGHTS
# Note: defines several areas with weights
# attempt to combine FEAR + EXPLORER + BRAKES
# does not work well, negative weights cancel positives and messes up. Removed.

def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")

    # MH: creates weighted quadrants
    mid_width = int(np.floor(shape[1]/2))
    thrd_height = int(np.floor(shape[0]/3))

    # MH: far away duckies are less relevant
    res[0:thrd_height, 0:mid_width] = 0.2
    res[0:thrd_height, mid_width:] = -0.2

    # MH: closer duckies are more relevant
    res[thrd_height:, 0:mid_width:] = 1.0
    res[thrd_height:, mid_width:] = -0.6

    return res


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    res = np.zeros(shape=shape, dtype="float32")

    # MH: creates weighted quadrants
    mid_width = int(np.floor(shape[1]/2))
    thrd_height = int(np.floor(shape[0]/3))

    # MH: far away duckies are less relevant
    res[0:thrd_height, 0:mid_width] = -0.2
    res[0:thrd_height, mid_width:] = 0.2

    # MH: closer duckies are more relevant
    res[thrd_height:, 0:mid_width:] = -0.6
    res[thrd_height:, mid_width:] = 1.0
    return res
"""
