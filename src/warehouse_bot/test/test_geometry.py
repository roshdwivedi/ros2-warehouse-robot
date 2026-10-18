import math

import pytest

from warehouse_bot.geometry import (
    distance_and_angle_to_goal,
    normalize_angle,
    yaw_from_quaternion,
)


def test_minus_340_becomes_20_degrees():
    result = normalize_angle(math.radians(-340))
    assert result == pytest.approx(math.radians(20))


def test_400_becomes_40_degrees():
    result = normalize_angle(math.radians(400))
    assert result == pytest.approx(math.radians(40))


def test_small_angle_unchanged():
    result = normalize_angle(math.radians(-20))
    assert result == pytest.approx(math.radians(-20))


def test_goal_3_4_triangle():
    distance, angle = distance_and_angle_to_goal(0, 0, 3, 4)
    assert distance == pytest.approx(5.0)
    assert angle == pytest.approx(math.atan2(4, 3))


def test_goal_straight_left():
    distance, angle = distance_and_angle_to_goal(1, 1, 1, 3)
    assert distance == pytest.approx(2.0)
    assert angle == pytest.approx(math.radians(90))


def test_goal_behind_right():
    distance, angle = distance_and_angle_to_goal(0, 0, -1, -1)
    assert distance == pytest.approx(math.sqrt(2))
    assert angle == pytest.approx(math.radians(-135))


def quaternion_from_yaw(yaw):
    """Build a flat-floor quaternion (x, y, z, w) for a given yaw."""
    return 0.0, 0.0, math.sin(yaw / 2), math.cos(yaw / 2)


def test_yaw_facing_left():
    x, y, z, w = quaternion_from_yaw(math.radians(90))
    assert yaw_from_quaternion(x, y, z, w) == pytest.approx(math.radians(90))


def test_yaw_facing_forward():
    x, y, z, w = quaternion_from_yaw(math.radians(0))
    assert yaw_from_quaternion(x, y, z, w) == pytest.approx(math.radians(0))


def test_yaw_facing_right():
    x, y, z, w = quaternion_from_yaw(math.radians(-90))
    assert yaw_from_quaternion(x, y, z, w) == pytest.approx(math.radians(-90))
