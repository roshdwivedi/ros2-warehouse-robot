import math


def normalize_angle(angle):
    """Return the angle wrapped into the range [-pi, pi]."""
    return (angle + math.pi) % (2 * math.pi) - math.pi


def distance_and_angle_to_goal(x, y, gx, gy):
    """Return (distance, angle) from the robot @ (x, y) to the goal @ (gx, gy)."""
    dx = gx - x
    dy = gy - y
    return math.hypot(dx, dy), math.atan2(dy, dx)


def yaw_from_quaternion(x, y, z, w):
    """Return the yaw of a quaternion, in radians."""
    return math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


def clamp(value, limit):
    """Return value limited to the range [-limit, limit]."""
    return max(-limit, min(value, limit))
