"""My personal utilities and settings for Matplotlib."""
from . import bounded, color, plot, style  # noqa: F401
from .bounded import Bounded
from .color import adjust_lightness, blend, brighter, darker, subcmap
from .plot import errorband, grid, line_annotate
from .style import colorblind, mystyle, mystyle_21_10, seaborn_colorblind_10, use
from .version import __version__

__all__ = (
    "Bounded",
    "__version__",
    "adjust_lightness",
    "blend",
    "brighter",
    "colorblind",
    "darker",
    "errorband",
    "grid",
    "line_annotate",
    "mystyle",
    "mystyle_21_10",
    "seaborn_colorblind_10",
    "subcmap",
    "use",
)
