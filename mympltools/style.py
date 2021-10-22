"""My Matplotlib styles."""
import collections.abc
import sys
from typing import Any, Dict, Optional, Sequence, Union

import cycler
import matplotlib.pyplot

__all__ = ("colorblind", "mystyle", "mystyle_21_10", "seaborn_colorblind_10", "use")

Style = Union[str, Dict[str, Any]]


# https://github.com/mwaskom/seaborn/blob/v0.11/seaborn/palettes.py#L40-L41
seaborn_colorblind_10 = {
    "axes.prop_cycle": cycler.cycler(
        color=[
            "#0173B2",
            "#DE8F05",
            "#029E73",
            "#D55E00",
            "#CC78BC",
            "#CA9161",
            "#FBAFE4",
            "#949494",
            "#ECE133",
            "#56B4E9",
        ]
    ),
}

mystyle_21_10 = {
    "axes.linewidth": 1.2,
    "font.size": 16,
    "grid.linestyle": ":",
    "legend.edgecolor": "0.0",
    "legend.fancybox": False,
    "legend.framealpha": 1,
    "lines.linewidth": 2,
    "lines.markersize": 6,
    "xtick.direction": "in",
    "xtick.major.bottom": True,
    "xtick.major.size": 5,
    "xtick.major.top": True,
    "xtick.major.width": 1,
    "xtick.minor.bottom": True,
    "xtick.minor.size": 3,
    "xtick.minor.top": True,
    "xtick.minor.visible": True,
    "xtick.minor.width": 1,
    "xtick.top": True,
    "ytick.direction": "in",
    "ytick.major.left": True,
    "ytick.major.right": True,
    "ytick.major.size": 5,
    "ytick.major.width": 1,
    "ytick.minor.left": True,
    "ytick.minor.right": True,
    "ytick.minor.size": 3,
    "ytick.minor.visible": True,
    "ytick.minor.width": 1,
    "ytick.right": True,
}

colorblind = seaborn_colorblind_10
mystyle = mystyle_21_10

matplotlib.pyplot.style.use([colorblind, mystyle])


def use(styles: Optional[Union[Style, Sequence[Style]]] = None) -> None:
    """Use the given styles."""
    if styles is None:
        matplotlib.pyplot.style.use("default")
        return
    if isinstance(styles, str) or not isinstance(styles, collections.abc.Sequence):
        styles = [styles]

    styles = [_get_style(style) for style in styles]

    matplotlib.pyplot.style.use(styles)


def _get_style(style: Style) -> Style:
    if isinstance(style, str):
        a = getattr(sys.modules[__name__], f"{style}", None)
        if isinstance(a, dict):
            return a
        a = getattr(sys.modules[__name__], f"mystyle_{style.replace('.', '_')}", None)
        if isinstance(a, dict):
            return a
        raise ValueError(f"style not found: {style}")
    return style
