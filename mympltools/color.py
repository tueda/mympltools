"""Color utility functions."""
import colorsys
from typing import Optional, Tuple, Union

import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np

__all__ = ("adjust_lightness", "blend", "brighter", "darker", "subcmap")

ColorRGB = Tuple[float, float, float]
Color = Union[str, ColorRGB]


def _get_color_rgb(color: Color) -> ColorRGB:
    """Return the RGB components of the given color."""
    try:
        c = matplotlib.colors.cnames[color]
    except KeyError:
        c = color
    return matplotlib.colors.to_rgb(c)  # type: ignore[no-any-return]


# https://stackoverflow.com/a/49601444
def adjust_lightness(color: Color, amount: float = 0.5) -> ColorRGB:
    """Adjust the lightness of the given color."""
    c = colorsys.rgb_to_hls(*_get_color_rgb(color))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def brighter(color: Color, amount: float = 0.7) -> ColorRGB:
    """Return a brighter color."""
    return adjust_lightness(color, 1 / amount)


def darker(color: Color, amount: float = 0.7) -> ColorRGB:
    """Return a darker color."""
    return adjust_lightness(color, amount)


def blend(color1: Color, color2: Color, ratio: float = 0.5) -> ColorRGB:
    """Return a blended color."""
    c1 = _get_color_rgb(color1)
    c2 = _get_color_rgb(color2)
    return (
        c1[0] * (1 - ratio) + c2[0] * ratio,
        c1[1] * (1 - ratio) + c2[1] * ratio,
        c1[2] * (1 - ratio) + c2[2] * ratio,
    )


# See also: https://stackoverflow.com/a/18926541
def subcmap(
    cmap: Union[matplotlib.colors.Colormap, str],
    minval: float = 0.0,
    maxval: float = 1.0,
    n: Optional[int] = None,
) -> matplotlib.colors.Colormap:
    """Return a part of the given color map."""
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    if n is None:
        n = cmap.N
    return matplotlib.colors.LinearSegmentedColormap.from_list(
        f"subcmap({cmap.name},{minval},{maxval})",
        cmap(np.linspace(minval, maxval, n)),
        n,
    )
