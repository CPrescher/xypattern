# -*- coding: utf-8 -*-
# Dioptas - GUI program for fast processing of 2D X-ray diffraction data
# Principal author: Clemens Prescher (clemens.prescher@gmail.com)
# Copyright (C) 2014-2019 GSECARS, University of Chicago, USA
# Copyright (C) 2015-2018 Institute for Geology and Mineralogy, University of Cologne, Germany
# Copyright (C) 2019-2020 DESY, Hamburg, Germany
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import numpy as np
import pytest
from pytest import approx
from xypattern.auto_background import SmoothBrucknerBackground

from xypattern.pattern import BkgNotInRangeError
from xypattern import Pattern

from .test_util import generate_peak_pattern, gaussian

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, "data")


def test_loading_chi_file():
    pattern = Pattern()
    x, y = pattern.data

    pattern.load(os.path.join(data_path, "pattern_001.chi"))
    new_x, new_y = pattern.data

    assert len(x) != len(new_x)
    assert len(y) != len(new_y)
    assert pattern.name == "pattern_001"
    assert pattern.filename == os.path.join(data_path, "pattern_001.chi")


def test_loading_invalid_file():
    pattern = Pattern()
    with pytest.raises(ValueError):
        pattern.load(os.path.join(data_path, "wrong_file_format.txt"))


def test_loading_from_file_chi():
    pattern = Pattern.from_file(os.path.join(data_path, "pattern_001.chi"))
    assert len(pattern.x) == 75
    assert len(pattern.y) == 75
    assert pattern.name == "pattern_001"
    assert pattern.filename == os.path.join(data_path, "pattern_001.chi")


def test_loading_from_file_invalid():
    with pytest.raises(ValueError):
        Pattern.from_file(os.path.join(data_path, "wrong_file_format.txt"))


def test_saving_a_dat_file(tmp_path):
    x = np.linspace(-5, 5, 100)
    y = x**2
    pattern = Pattern(x, y)
    filename = os.path.join(tmp_path, "test.dat")
    pattern.save(filename)

    pattern2 = Pattern()
    pattern2.load(filename)

    pattern2_x, pattern2_y = pattern2.data
    assert pattern2_x == pytest.approx(x)
    assert pattern2_y == pytest.approx(y)


def test_saving_a_chi_file(tmp_path):
    x = np.linspace(-5, 5, 100)
    y = x**2
    pattern = Pattern(x, y)
    filename = os.path.join(tmp_path, "test.chi")
    pattern.save(filename)

    pattern2 = Pattern()
    pattern2.load(filename)

    pattern2_x, pattern2_y = pattern2.data
    assert pattern2_x == pytest.approx(x)
    assert pattern2_y == pytest.approx(y)

    with open(filename) as f:
        lines = f.readlines()
        assert lines[0].endswith("test.chi\n")
        assert lines[1] == "2th_deg\n"
        assert lines[3].endswith(f"{len(pattern2_x)}\n")


def test_saving_a_fxye_file(tmp_path):
    x = np.linspace(-5, 5, 100)
    y = x**2
    pattern = Pattern(x, y)
    filename = os.path.join(tmp_path, "test.fxye")
    pattern.save(filename)


def test_saving_a_chi_file_with_background(tmp_path):
    x = np.linspace(-5, 5, 100)
    y = x**2

    pattern = Pattern(x, y)
    pattern.background_pattern = Pattern(x, x)
    filename = os.path.join(tmp_path, "test.chi")
    pattern.save(filename, subtract_background=True)

    assert os.path.exists(filename)
    pattern_saved = Pattern.from_file(filename)
    assert pattern_saved.background_pattern is None
    assert pattern_saved.x == pytest.approx(x)
    assert pattern_saved.y == pytest.approx(y - x)


def test_saving_a_chi_file_with_auto_bkg(tmp_path):
    x = np.linspace(-5, 5, 100)
    y = x**2

    pattern = Pattern(x, y)
    pattern.auto_bkg = SmoothBrucknerBackground()
    filename = os.path.join(tmp_path, "test.chi")
    pattern.save(filename, subtract_background=True)

    assert os.path.exists(filename)
    pattern_saved = Pattern.from_file(filename)
    assert pattern_saved.background_pattern is None
    assert pattern_saved.x == pytest.approx(x)
    assert pattern_saved.y == pytest.approx(y - pattern.auto_background_pattern.y)


def test_saving_a_chi_file_with_auto_bkg_and_subtract_background_false(tmp_path):
    x = np.linspace(-5, 5, 100)
    y = x**2

    pattern = Pattern(x, y)
    pattern.auto_bkg = SmoothBrucknerBackground()
    filename = os.path.join(tmp_path, "test.chi")
    pattern.save(filename, subtract_background=False)

    assert os.path.exists(filename)
    pattern_saved = Pattern.from_file(filename)
    assert pattern_saved.background_pattern is None
    assert pattern_saved.x == pytest.approx(x)
    assert pattern_saved.y == pytest.approx(y)


def test_plus_and_minus_operators():
    x = np.linspace(0, 10, 100)
    pattern1 = Pattern(x, np.sin(x))
    pattern2 = Pattern(x, np.sin(x))

    pattern3 = pattern1 + pattern2
    assert np.array_equal(pattern3.y, np.sin(x) * 2)
    assert np.array_equal(pattern2._original_y, np.sin(x) * 1)
    assert np.array_equal(pattern1._original_y, np.sin(x) * 1)

    pattern3 = pattern1 + pattern1
    assert np.array_equal(pattern3.y, np.sin(x) * 2)
    assert np.array_equal(pattern1._original_y, np.sin(x) * 1)
    assert np.array_equal(pattern1._original_y, np.sin(x) * 1)

    pattern3 = pattern2 - pattern1
    assert np.array_equal(pattern3.y, np.sin(x) * 0)
    assert np.array_equal(pattern2._original_y, np.sin(x) * 1)
    assert np.array_equal(pattern1._original_y, np.sin(x) * 1)

    pattern3 = pattern1 - pattern1
    assert np.array_equal(pattern3.y, np.sin(x) * 0)
    assert np.array_equal(pattern1._original_y, np.sin(x) * 1)
    assert np.array_equal(pattern1._original_y, np.sin(x) * 1)


def test_plus_and_minus_operators_with_different_shapes():
    x = np.linspace(0, 10, 1000)
    x2 = np.linspace(0, 12, 1300)
    pattern1 = Pattern(x, np.sin(x))
    pattern2 = Pattern(x2, np.sin(x2))
    pattern3 = pattern1 + pattern2

    assert pattern3.x == approx(pattern1._original_x)
    assert pattern3.y == approx(pattern1._original_y * 2, abs=1e-4)

    pattern3 = pattern1 + pattern1
    assert pattern3.y == approx(np.sin(x) * 2, abs=1e-4)

    pattern3 = pattern1 - pattern2
    assert pattern3.y == approx(np.sin(x) * 0, abs=1e-4)

    pattern3 = pattern1 - pattern1
    assert pattern3.y == approx(np.sin(x) * 0, abs=1e-4)


def test_multiply_with_scalar_operator():
    x = np.linspace(0, 10, 100)
    pattern = 2 * Pattern(x, np.sin(x))
    assert np.array_equal(pattern.y, np.sin(x) * 2)


def test_using_background_pattern():
    x = np.linspace(-5, 5, 100)
    pattern_y = x**2
    bkg_y = x

    spec = Pattern(x, pattern_y)
    background_pattern = Pattern(x, bkg_y)

    spec.background_pattern = background_pattern
    new_x, new_y = spec.data

    assert np.array_equal(new_x, x)
    assert np.array_equal(new_y, pattern_y - bkg_y)


def test_using_background_pattern_with_different_spacing():
    x = np.linspace(-5, 5, 100)
    pattern_y = x**2
    x_bkg = np.linspace(-5, 5, 99)
    bkg_y = x_bkg

    spec = Pattern(x, pattern_y)
    background_pattern = Pattern(x_bkg, bkg_y)

    spec.background_pattern = background_pattern
    new_x, new_y = spec.data

    assert np.array_equal(new_x, x)
    assert np.array_equal(new_y, pattern_y - x)


def test_changing_the_background_pattern_parameters():
    x = np.linspace(-5, 5, 100)
    pattern_y = x**2
    bkg_y = x

    spec = Pattern(x, pattern_y)
    background_pattern = Pattern(x, bkg_y)

    spec.background_pattern = background_pattern
    new_x, new_y = spec.data

    assert np.array_equal(new_x, x)
    assert np.array_equal(new_y, pattern_y - bkg_y)

    background_pattern.offset = 100
    new_x, new_y = spec.data
    assert np.array_equal(background_pattern.y, bkg_y + 100)
    assert np.array_equal(background_pattern.data[1], bkg_y + 100)
    assert np.array_equal(new_y, pattern_y - (bkg_y + 100))


def test_changing_the_background_pattern_to_new_background():
    x = np.linspace(-5, 5, 100)
    pattern_y = x**2
    bkg_y = x

    pattern = Pattern(x, pattern_y)
    background_pattern = Pattern(x, bkg_y)

    pattern.background_pattern = background_pattern
    assert len(background_pattern.changed.listeners) == 1

    background_pattern2 = Pattern(x, bkg_y + 100)
    pattern.background_pattern = background_pattern2
    assert len(background_pattern.changed.listeners) == 0
    assert len(background_pattern2.changed.listeners) == 1

    pattern.background_pattern = None
    assert len(background_pattern.changed.listeners) == 0
    assert len(background_pattern2.changed.listeners) == 0


def test_background_out_of_range_throws_error():
    x1 = np.linspace(0, 10)
    x2 = np.linspace(-10, -1)

    spec = Pattern(x1, x1)
    background_pattern = Pattern(x2, x2)

    with pytest.raises(BkgNotInRangeError):
        spec.background_pattern = background_pattern


def test_automatic_background_subtraction():
    pattern, y_bkg = generate_peak_pattern(with_bkg=True)
    without_bkg_y = pattern.y - y_bkg

    pattern.auto_bkg = SmoothBrucknerBackground(2, 50, 50)

    _, y_spec = pattern.data
    assert y_spec == approx(without_bkg_y, abs=1e-4)


def test_automatic_background_subtraction_with_roi():
    pattern = generate_peak_pattern()
    roi = [1, 23]
    pattern.auto_bkg_roi = roi
    pattern.auto_bkg = SmoothBrucknerBackground(2, 50, 50)

    x_spec, _ = pattern.data

    assert x_spec[0] > roi[0]
    assert x_spec[-1] < roi[1]


def test_setting_new_data():
    spec = Pattern()
    x = np.linspace(0, 10)
    y = np.sin(x)
    spec.data = x, y

    new_x, new_y = spec.data
    assert np.array_equal(new_x, x)
    assert np.array_equal(new_y, y)


def test_using_len():
    x = np.linspace(0, 10, 234)
    y = x**2
    spec = Pattern(x, y)

    assert len(spec) == 234


def test_scaling():
    x = np.linspace(0, 10, 100)
    pattern = Pattern(x, np.sin(x))
    pattern.scaling = 2
    assert np.array_equal(pattern.y, np.sin(x) * 2)


def test_multiply_operator():
    x = np.linspace(0, 10, 100)
    pattern = 2 * Pattern(x, np.sin(x))

    assert np.array_equal(pattern._original_y, np.sin(x) * 2)


def test_equality_operator():
    x = np.linspace(0, 10, 100)
    pattern1 = Pattern(x, np.sin(x))
    pattern2 = Pattern(x, np.sin(2 * x))

    assert pattern1 == pattern1
    assert pattern1 != pattern2


def test_binning():
    x = np.linspace(2.8, 10.8, 100)
    pattern = Pattern(x, np.sin(x))
    binned_pattern = pattern.rebin(1)
    assert np.sum(binned_pattern.y), np.sum(pattern.y)


def test_extend_to():
    x = np.arange(2.8, 10, 0.2)

    pattern = Pattern(x, x - 2)
    extended_pattern = pattern.extend_to(0, 0)

    assert np.sum(extended_pattern.limit(0, 2.7).y) == approx(0)
    assert extended_pattern.x[0] == approx(0)

    pos_extended_pattern = pattern.extend_to(20, 5)

    assert np.mean(pos_extended_pattern.limit(10.1, 21).y) == 5
    assert pos_extended_pattern.x[-1] == approx(20)


def test_to_dict():
    pattern = Pattern(np.arange(10), np.arange(10))
    pattern.name = "test"
    pattern.scaling = 3
    pattern.smoothing = 2
    pattern._background_pattern = Pattern(np.arange(10), np.arange(10))
    pattern_json = pattern.to_dict()
    assert pattern_json["x"] == list(pattern._original_x)
    assert pattern_json["y"] == list(pattern._original_y)
    assert pattern_json["name"] == pattern.name
    assert pattern_json["scaling"] == pattern.scaling
    assert pattern_json["smoothing"] == pattern.smoothing
    assert pattern_json["bkg_pattern"] == pattern._background_pattern.to_dict()


def test_from_dict():
    pattern1 = Pattern(np.arange(10), np.arange(10))
    pattern1.name = "test"
    pattern1.scaling = 3
    pattern1.smoothing = 2
    pattern1.background_pattern = Pattern(np.arange(10), np.arange(10))
    pattern_json = pattern1.to_dict()

    pattern2 = Pattern.from_dict(pattern_json)
    assert np.array_equal(pattern1.x, pattern2.x)
    assert np.array_equal(pattern1.y, pattern2.y)
    assert pattern1.name == pattern2.name
    assert pattern1.scaling == pattern2.scaling
    assert pattern1.smoothing == pattern2.smoothing
    assert np.array_equal(
        pattern1._background_pattern.x, pattern2._background_pattern.x
    )
    assert np.array_equal(
        pattern1._background_pattern.y, pattern2._background_pattern.y
    )


def test_str_representation():
    pattern = Pattern(np.arange(10), np.arange(10), name="test")
    assert str(pattern) == "Pattern 'test' with 10 points"


def test_delete_range():
    pattern = Pattern(np.arange(11), np.arange(11), name="test")
    pattern = pattern.delete_range([2.3, 7.9])
    assert np.array_equal(pattern.x, np.array([0, 1, 2, 8, 9, 10]))
    assert np.array_equal(pattern.y, np.array([0, 1, 2, 8, 9, 10]))


def test_delete_ranges():
    pattern = Pattern(np.arange(31), np.arange(31), name="test")
    pattern = pattern.delete_ranges([[4.4, 13.3]])
    assert np.array_equal(pattern.x, np.concatenate((np.arange(5), np.arange(14, 31))))

    pattern = pattern.delete_ranges(
        [[3.9, 13.6], [4.5, 14.4], [21.5, 24.9], [27.1, 29.5]]
    )
    assert np.array_equal(
        pattern.x,
        np.concatenate(
            (np.arange(4), np.arange(15, 22), np.arange(25, 28), np.array([30]))
        ),
    )


def test_transform_x():
    x = np.linspace(0, 10, 100)
    pattern = Pattern(x, np.sin(x))
    pattern.transform_x(lambda x: x + 2)
    assert np.array_equal(pattern.x, x + 2)


def test_transform_x_with_pattern_bkg():
    x = np.linspace(0, 10, 100)
    pattern = Pattern(x, np.sin(x))
    pattern.background_pattern = Pattern(x, np.cos(x))
    pattern.transform_x(lambda x: x + 2)

    assert np.array_equal(pattern.x, x + 2)
    assert np.array_equal(pattern.background_pattern.x, x + 2)


def test_transform_x_with_auto_bkg():
    x = np.linspace(0, 10, 100)
    pattern = Pattern(x, np.sin(x))
    pattern.auto_bkg = SmoothBrucknerBackground()
    pattern.transform_x(lambda x: x + 2)
    assert np.array_equal(pattern.x, x + 2)


def test_copy_basic():
    """Test that the copy method creates a new Pattern with the same data."""
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    pattern = Pattern(x, y, name="test_pattern")
    
    # Set some properties
    pattern.scaling = 2.0
    pattern.offset = 1.0
    pattern.smoothing = 0.5
    
    # Create a copy
    pattern_copy = pattern.copy()
    
    # Check that the copy has the same properties
    assert pattern_copy.name == pattern.name
    assert np.array_equal(pattern_copy.x, pattern.x)
    assert np.array_equal(pattern_copy.y, pattern.y)
    assert pattern_copy.scaling == pattern.scaling
    assert pattern_copy.offset == pattern.offset
    assert pattern_copy.smoothing == pattern.smoothing
    
    # Check that it's a deep copy by modifying the original
    pattern.scaling = 3.0
    pattern.offset = 2.0
    pattern.smoothing = 1.0
    pattern.name = "modified_pattern"
    
    # The copy should not be affected
    assert pattern_copy.name == "test_pattern"
    assert pattern_copy.scaling == 2.0
    assert pattern_copy.offset == 1.0
    assert pattern_copy.smoothing == 0.5


def test_copy_with_background():
    """Test that the copy method properly handles background patterns."""
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    pattern = Pattern(x, y, name="test_pattern")
    
    # Create a background pattern
    bkg = Pattern(x, 0.1 * x, name="background")
    pattern.background_pattern = bkg
    
    # Create a copy
    pattern_copy = pattern.copy()
    
    # Check that the background was copied
    assert pattern_copy.background_pattern is not None
    assert pattern_copy.background_pattern.name == "background"
    assert np.array_equal(pattern_copy.background_pattern.x, bkg.x)
    assert np.array_equal(pattern_copy.background_pattern.y, bkg.y)
    
    # Check that it's a deep copy by modifying the original background
    pattern.background_pattern.name = "modified_background"
    
    # The copy's background should not be affected
    assert pattern_copy.background_pattern.name == "background"


def test_copy_with_auto_background():
    """Test that the copy method properly handles auto background settings."""
    x = np.linspace(0, 10, 100)
    y = np.sin(x) + x * 0.1  # Add a linear background
    pattern = Pattern(x, y, name="test_pattern")
    
    # Set auto background
    pattern.auto_bkg = SmoothBrucknerBackground(smooth_width=0.2, iterations=30, cheb_order=20)
    pattern.auto_bkg_roi = [1.0, 9.0]
    
    # Create a copy
    pattern_copy = pattern.copy()
    
    # Check that the auto background settings were copied
    assert pattern_copy.auto_bkg is not None
    assert pattern_copy.auto_bkg_roi == pattern.auto_bkg_roi
    assert pattern_copy.auto_bkg.smooth_width == pattern.auto_bkg.smooth_width
    assert pattern_copy.auto_bkg.iterations == pattern.auto_bkg.iterations
    assert pattern_copy.auto_bkg.cheb_order == pattern.auto_bkg.cheb_order
    
    # Check that it's a deep copy by modifying the original
    pattern.auto_bkg.smooth_width = 0.5
    pattern.auto_bkg_roi = [2.0, 8.0]
    
    # The copy should not be affected
    assert pattern_copy.auto_bkg_roi == [1.0, 9.0]
    assert pattern_copy.auto_bkg.smooth_width == 0.2
