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