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

x = np.linspace(-5, 5)
y = np.exp(x)

fig, ax = plt.subplots()
l = ax.plot(x, y)
mt.line_annotate("awesome function", l)
ax.set_yscale("log")
mt.grid(ax)
plt.show()
```

See more [examples](https://github.com/tueda/mympltools/blob/main/examples/Examples.ipynb).


Development
-----------

```bash
poetry install
poetry run task prepare
```
