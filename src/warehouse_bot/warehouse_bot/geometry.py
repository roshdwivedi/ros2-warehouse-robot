import math


def normalize_angle(angle):
    """Return the angle wrapped into the range [-pi, pi]."""
    return (angle + math.pi) % (2*math.pi) - math.pi
