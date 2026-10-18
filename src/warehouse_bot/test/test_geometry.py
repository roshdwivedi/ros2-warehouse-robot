import math

import pytest

from warehouse_bot.geometry import normalize_angle


def test_minus_340_becomes_20_degrees():
    result = normalize_angle(math.radians(-340))
    assert result == pytest.approx(math.radians(20))


def test_400_becomes_40_degrees():
    result = normalize_angle(math.radians(400))
    assert result == pytest.approx(math.radians(40))


def test_small_angle_unchanged():
    result = normalize_angle(math.radians(-20))
    assert result == pytest.approx(math.radians(-20))
