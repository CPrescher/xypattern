=====
Usage
=====

This page provides examples of how to use the xypattern library.

Reading a file
--------------

.. code-block:: python

    from xypattern import Pattern
    import matplotlib.pyplot as plt

    p1 = Pattern.from_file('path/to/file')
    p1.scaling = 0.5
    p1.offset = 0.1

    plt.plot(p1.x, p1.y)
    plt.show()

Using a background pattern
--------------------------

.. code-block:: python

    p2 = Pattern.from_file('path/to/file')
    p2.scaling = 0.9
    p1.background_pattern = p2

Automatic background subtraction
--------------------------------

.. code-block:: python

    from xypattern.auto_background import SmoothBrucknerBackground

    p1 = Pattern.from_file('path/to/file')
    p1.auto_bkg = SmoothBrucknerBackground(smooth_width=0.2, iterations=30, cheb_order=20)
    p1.auto_bkg_roi = [10.0, 60.0]  # Optional region of interest for background calculation

Pattern manipulation
--------------------

.. code-block:: python

    # Limit pattern to a specific x-range
    limited_pattern = p1.limit(10.0, 60.0)

    # Extend pattern to a specific x-value
    extended_pattern = p1.extend_to(5.0, 0.0)

    # Delete specific x-ranges
    cleaned_pattern = p1.delete_ranges([[10.0, 15.0], [40.0, 45.0]])

    # Transform x-axis (e.g., convert from 2theta to q-space)
    from math import pi, sin
    wavelength = 0.3344  # Å
    transformed_pattern = p1.transform_x(lambda x: 4 * pi * sin(x * pi / 360) / wavelength)

Scale and stitch multiple patterns
----------------------------------

.. code-block:: python

    p1 = Pattern.from_file('path/to/file1')
    p2 = Pattern.from_file('path/to/file2')
    p3 = Pattern.from_file('path/to/file3')

    from xypattern.combine import scale_patterns, stitch_patterns

    patterns = [p1, p2, p3]
    scale_patterns(patterns)
    stitched_pattern = stitch_patterns(patterns)

Pattern serialization
---------------------

.. code-block:: python

    # Save pattern to dictionary (useful for JSON serialization)
    pattern_dict = p1.to_dict()

    # Create pattern from dictionary
    p2 = Pattern.from_dict(pattern_dict)

    # Create a deep copy of a pattern
    p2 = p1.copy() 