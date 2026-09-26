============
Installation
============

xypattern can be installed using pip:

.. code-block:: bash

    pip install xypattern

Requirements
------------

xypattern requires:

* Python 3.8–3.14
* NumPy
* SciPy

Python 3.15 has prerelease support, tested with 3.15.0rc2. It requires NumPy
>= 2.5.2, SciPy >= 1.18.1, and Cython >= 3.3 for source builds.

On Python 3.14, NumPy >= 2.3.3 and SciPy >= 1.16.1 are required. pip
automatically selects compatible versions. Building from source requires a C
compiler for the Cython extension.

Development Installation
------------------------

For development, you can clone the repository and install it in development mode:

.. code-block:: bash

    git clone https://github.com/CPrescher/xypattern.git
    cd xypattern
    poetry env use python3.14
    poetry install
