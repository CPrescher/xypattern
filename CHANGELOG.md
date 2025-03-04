# 1.2.0 (in progress)

- adding and subtracting patterns with different x-values will now work both with linear interpolation (before subtraction was using cubic interpolation and adding linear)
- pattern to_dict and from_dict now also save and restore auto_bkg and auto_bkg_roi
- added a copy method to pattern class

# 1.1.2 (2024-03-14)

- now correctly saves a file without background (subtract_background parameter false) when auto_bkg is set

# 1.1.1 (2024-03-13)

- fixed inclusion of compiled smooth bruckner functions in wheels on linux and macos

# 1.1.0 (2024-03-13)

- added feature to delete a range in a pattern
- added filename field in pattern, which contains complete filepath (name will still just hold the name)
- added transform_x function to modify the x-axis in place (will also update backgrounds)
- changed the auto background api, new usage:
```python
  pattern.auto_bkg = SmoothBrucknerBackground()
  pattern.auto_bkg_roi = [10, 20]
  pattern.auto_bkg = None # will switch it off
```

# 1.0.5 (2013-11-14)

- enable poetry versioning plugin during build, to hopefully work when installing with pypi

# 1.0.4 (2023-11-13)

 - fix constraints to also actually work with python 3.8

# 1.0.3 (2023-11-13)

- provide packages for python 3.8 to 3.12

# 1.0.2 (2023-10-14)

## Bugfixes
- fix out of bound error for find_scaling (will be extrapolated in case there is a tiny mismatch in the binning)

# 1.0.1 (2023-10-14)

## new features
- find_scaling (and in accord also scale_patterns) works now with patterns that have different binning in the 
  overlapping region

# 1.0.0 (2023-10-13)

Initial Release