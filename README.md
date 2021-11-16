mympltools
==========

My personal utilities and settings for [Matplotlib](https://matplotlib.org/).


Getting Started
---------------

[Pip](https://pip.pypa.io/en/stable/):
```bash
pip install git+https://github.com/tueda/mympltools.git@21.11.0
```

[Poetry](https://python-poetry.org/):
```bash
poetry add git+https://github.com/tueda/mympltools.git@21.11.0
```

It is recommended to specify the version completely in case of future incompatible changes.


Examples
--------

```python
import matplotlib.pyplot as plt
import numpy as np
import mympltools as mt

mt.use("21.10")  # Use the style.

fig, ax = plt.subplots()
x = np.linspace(-5, 5)
ax.plot(x, x ** 2)
mt.grid(ax)  # Show grid lines.
plt.show()
```

See more [examples](https://github.com/tueda/mympltools/blob/main/examples/Examples.ipynb).


Similar Software
----------------

You may also be interested in the following packages.

- [`mpltools`](https://github.com/tonysyu/mpltools): tools for Matplotlib.

- [`mplhep`](https://github.com/scikit-hep/mplhep): tools and HEP styles (ALICE, ATLAS, CMS, LHCb and [more](https://github.com/scikit-hep/mplhep/blob/fd3d12414f73b46d3955ccca38af2cc7ccf48961/src/mplhep/styles/__init__.py#L88-L90)).


Development
-----------

```bash
poetry install
poetry run task prepare
```
