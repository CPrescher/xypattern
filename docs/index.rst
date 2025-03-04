.. xypattern documentation master file, created by
   sphinx-quickstart on Tue Mar  4 11:56:29 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to xypattern's documentation!
=====================================

xypattern is a simple small library to handle x-y patterns, such as those collected with x-ray diffraction or Raman spectroscopy.

Features
--------

- Load and save patterns from/to various file formats (.xy, .chi, .fxye)
- Apply scaling, offset, and smoothing to patterns
- Background subtraction (manual or automatic)
- Pattern manipulation (limiting, extending, deleting ranges)
- Mathematical operations (addition, subtraction, multiplication)
- Pattern transformation (x-axis transformation)
- Pattern rebinning
- Pattern serialization to/from dictionaries

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
