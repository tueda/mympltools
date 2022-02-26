"""Utility functions for plotting."""
from typing import Any, List, Optional, Tuple, Union

import matplotlib.axes
import matplotlib.collections
import matplotlib.lines
import numpy as np

from .npt_compat import ArrayLike, NDArray1D, NDArray2D

__all__ = ("errorband", "grid", "line_annotate")


def grid(ax: matplotlib.axes.Axes) -> None:
    """Show grid lines."""
    # Grid line styles should be configured programmatically.
    # https://github.com/matplotlib/matplotlib/issues/13919
    ax.grid(which="major", linestyle="-", color="0.8")
    ax.grid(which="minor", linestyle=":", color="0.8")

    # Redraw ticks after all elements in the plot are drawn.
    ax.set_axisbelow(True)
    ax.add_artist(TickRedrawer())

    # Use `10` and `1` instead of `10^1` and `10^0`, respectively, in tick labels.
    for axis in (ax.xaxis, ax.yaxis):
        if isinstance(
            axis.get_major_formatter(), matplotlib.ticker.LogFormatterSciNotation
        ):
            axis.set_major_formatter(LogFormatterSciNotation2())


# https://stackoverflow.com/a/68608562
class TickRedrawer(matplotlib.artist.Artist):  # type: ignore[misc]
    """Artist to redraw ticks."""

    __name__ = "ticks"

    zorder = 10

    @matplotlib.artist.allow_rasterization  # type: ignore[misc]
    def draw(self, renderer: matplotlib.backend_bases.RendererBase) -> None:
        """Draw the ticks."""
        if not self.get_visible():
            self.stale = False
            return

        renderer.open_group(self.__name__, gid=self.get_gid())

        for axis in (self.axes.xaxis, self.axes.yaxis):
            loc_min, loc_max = axis.get_view_interval()

            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                if tick.get_visible() and loc_min <= tick.get_loc() <= loc_max:
                    for artist in (tick.tick1line, tick.tick2line):
                        artist.draw(renderer)

        renderer.close_group(self.__name__)
        self.stale = False


class LogFormatterSciNotation2(
    matplotlib.ticker.LogFormatterSciNotation  # type: ignore[misc]
):
    """Modified `LogFormatterSciNotation`."""

    def __call__(self, x: float, pos: Optional[int] = None) -> str:
        """Return the format for `x` at `pos`."""
        if x not in [1, 10]:
            return super().__call__(x, pos=pos)  # type: ignore[no-any-return]
        else:
            return f"{x:g}"


def errorband(
    ax: matplotlib.axes.Axes,
    x: ArrayLike,
    y: ArrayLike,
    yerr: Optional[ArrayLike] = None,
    alpha: float = 0.3,
    **kwargs: Any,
) -> Tuple[Union[matplotlib.lines.Line2D, matplotlib.collections.PolyCollection]]:
    """Plot `y` versus `x` with an error band."""
    if yerr is None:
        return tuple(ax.plot(x, y, **kwargs))  # type: ignore[return-value]

    kwargs1 = kwargs
    kwargs2 = kwargs.copy()

    (art1,) = ax.plot(x, y, **kwargs1)

    kwargs2.pop("c", None)
    kwargs2.pop("label", None)
    kwargs2.pop("linestyle", None)

    kwargs2.update(color=art1.get_color(), linestyle="solid")

    x = np.atleast_1d(x)
    y = np.atleast_1d(y)
    yerr = np.atleast_1d(yerr)

    if len(yerr.shape) == 2 and yerr.shape[0] == 2:
        yerr1 = yerr[0, :]
        yerr2 = yerr[1, :]
    else:
        yerr1 = yerr
        yerr2 = yerr

    art2 = ax.fill_between(
        x,
        y - yerr1,
        y + yerr2,
        alpha=alpha,
        **kwargs2,
    )

    return art1, art2  # type: ignore[return-value]


# Based on https://stackoverflow.com/a/64707070
# Changes:
# - `line` can be a list (the return value of `ax.plot`).
# - Use ``c=line.get_color()`` by default.
# - `x` can be omitted.
# - `x2` and `xytext` added.
def line_annotate(
    text: str,
    line: Union[matplotlib.lines.Line2D, List[matplotlib.lines.Line2D]],
    x: Optional[float] = None,
    x2: Optional[float] = None,
    xytext: Tuple[float, float] = (0, 5),
    *args: Any,
    **kwargs: Any,
) -> "LineAnnotation":
    """Add a sloped annotation to `line` at position `x` with `text`."""
    # Allow the return value of `matplotlib.axes.Axes.plot()`.
    if isinstance(line, list):
        if len(line) == 1:
            line = line[0]

    # Use the line color by default.
    if "c" not in kwargs and "color" not in kwargs:
        kwargs.update(c=line.get_color())

    ax = line.axes
    a = LineAnnotation(text, line, x, x2, xytext, *args, **kwargs)
    if "clip_on" in kwargs:
        a.set_clip_path(ax.patch)
    ax.add_artist(a)

    return a


# Based on https://stackoverflow.com/a/64707070
# Changes:
# - `x` can be omitted.
# - `x2` added.
# - `rotation` works.
class LineAnnotation(matplotlib.text.Annotation):  # type: ignore[misc]
    """Annotation to a line."""

    def __init__(
        self,
        text: str,
        line: matplotlib.lines.Line2D,
        x: Optional[float],
        x2: Optional[float],
        xytext: Tuple[float, float],
        textcoords: str = "offset points",
        **kwargs: Any,
    ) -> None:
        """Construct an annotation."""
        if not textcoords.startswith("offset "):
            raise ValueError("'textcoords' must be 'offset points' or 'offset pixels'")

        self._line = line
        self._xytext = xytext

        # Determine points of the line immediately to the left and right of x.
        xs, ys = line.get_data()

        if len(xs) == 0:
            raise ValueError("no points in the line")

        xmin = min(xs)
        xmax = max(xs)

        if x is None:
            x = (xmin + xmax) / 2
        elif x <= xmin:
            x = np.nextafter(xmin, xmax)
        elif x >= xmax:
            x = np.nextafter(xmax, xmin)

        if x2 is not None:
            if x2 <= xmin:
                x2 = np.nextafter(xmin, xmax)
            elif x2 >= xmax:
                x2 = np.nextafter(xmax, xmin)

        if x is None:
            raise AssertionError("x is None")

        def find_neighbors(
            x: float, xs: NDArray1D, ys: NDArray1D, reverse: bool = True
        ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
            (indices,) = np.where((xs <= x)[:-1] & (xs > x)[1:])
            if len(indices) == 0:
                if not reverse:
                    raise AssertionError("line must cross x")
                return find_neighbors(x, xs[::-1], ys[::-1], reverse=False)

            i = indices[0]
            return (xs[i], ys[i]), (xs[i + 1], ys[i + 1])

        if len(xs) == 1:
            n1 = xs[0], ys[0]
            n2 = xs[0] + 1, ys[0]
        elif x2 is None:
            n1, n2 = find_neighbors(x, xs, ys)
        else:
            n1, _ = find_neighbors(x, xs, ys)
            n2, n3 = find_neighbors(x2, xs, ys)
            if np.isclose(n1[0], n2[0]):
                if np.isclose(n1[0], n3[0]):
                    n2 = n1[0] + 1, n1[1]
                else:
                    n2 = n3
        self._neighbours: NDArray2D = np.asarray([n1, n2])
        print(self._neighbours)

        # Calculate y by interpolating neighbouring points.
        y = n1[1] + ((x - n1[0]) * (n2[1] - n1[1]) / (n2[0] - n1[0]))

        kwargs = {
            "horizontalalignment": "center",
            "rotation_mode": "anchor",
            **kwargs,
        }
        super().__init__(text, (x, y), xytext=xytext, textcoords=textcoords, **kwargs)

    def get_rotation(self) -> float:
        """Determine the angle of the slope of the neighbours."""
        trans_data = self._line.get_transform()
        dx, dy = np.diff(trans_data.transform(self._neighbours), axis=0).squeeze()
        return float(np.rad2deg(np.arctan2(dy, dx)) + super().get_rotation())

    def update_positions(self, renderer: matplotlib.backend_bases.RendererBase) -> None:
        """Update the relative position of the annotation text."""
        xytext = (
            matplotlib.transforms.Affine2D()
            .rotate_deg(self.get_rotation() - super().get_rotation())
            .transform(self._xytext)
        )
        self.set_position(xytext)
        super().update_positions(renderer)
