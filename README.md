mympltools
==========

My personal utilities and settings for [Matplotlib](https://matplotlib.org/).


Getting Started
---------------

[Pip](https://pip.pypa.io/en/stable/):
```bash
pip install git+https://github.com/tueda/mympltools.git@21.10.1
```

[Poetry](https://python-poetry.org/):
```bash
poetry add git+https://github.com/tueda/mympltools.git@21.10.1
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


Development
-----------

```bash
poetry install
poetry run task prepare
```
