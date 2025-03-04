import pytest
from xypattern.auto_background import SmoothBrucknerBackground


def test_transform_x():
    bkg = SmoothBrucknerBackground()

    assert bkg.smooth_width == 0.1
    bkg.transform_x(lambda x: x**2)
    assert bkg.smooth_width == pytest.approx(0.1**2)
    assert bkg.iterations == 50
    assert bkg.cheb_order == 50
