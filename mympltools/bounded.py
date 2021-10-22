"""Routines to handle uncertainties by the interval arithmetic."""
import dataclasses
from typing import Any, Optional, Union, cast, overload

import numpy as np

from .npt_compat import ArrayLike, NDArray1D, NDArray2D

__all__ = ("Bounded",)


@dataclasses.dataclass(init=False, eq=False, frozen=True)
class Bounded:
    """Numbers bounded by lower and upper limits of uncertainty."""

    x: NDArray1D
    x1: NDArray1D
    x2: NDArray1D

    @overload
    def __init__(self, x: ArrayLike) -> None:  # noqa: D107
        ...

    @overload
    def __init__(self, x: ArrayLike, dx: ArrayLike) -> None:  # noqa: D107
        ...

    @overload
    def __init__(  # noqa: D107
        self, x: ArrayLike, dx: ArrayLike, dx2: ArrayLike
    ) -> None:
        ...

    @overload
    def __init__(  # noqa: D107
        self, x: ArrayLike, *, xlo: ArrayLike, xhi: ArrayLike
    ) -> None:
        ...

    @overload
    def __init__(self, x: ArrayLike, *, xs: ArrayLike) -> None:  # noqa: D107
        ...

    def __init__(
        self,
        x: ArrayLike,
        dx: Optional[ArrayLike] = None,
        dx2: Optional[ArrayLike] = None,
        xlo: Optional[ArrayLike] = None,
        xhi: Optional[ArrayLike] = None,
        xs: Optional[ArrayLike] = None,
    ) -> None:
        """Construct a number/numbers bounded by lower/upper limits of uncertainty."""
        # Allowed combinations of the arguments:
        # - x           -> [x, x, x]
        # - x, dx       -> [x, x - abs(dx), x + abs(dx)]
        # - x, dx, dx2  -> [x, x - abs(dx), x + abs(dx2)]
        # - x, xlo, xhi -> [x, xlo, xhi]
        # - x, xs       -> [x, min(xs), max(xs)]

        x = np.atleast_1d(x)
        if len(x.shape) == 2:
            if dx is not None or dx2 is not None:
                raise ValueError("2-dimensional x cannot be used with dx or dx2")
            if x.shape[1] == 2:
                # 2 columns.
                dx = x[:, 1]
                x = x[:, 0]
                x = cast(NDArray1D, x)
            elif x.shape[1] == 3:
                # 3 columns.
                dx = x[:, 1]
                dx2 = x[:, 2]
                x = x[:, 0]
                x = cast(NDArray1D, x)
            else:
                raise ValueError(f"x has invalid shape: {x.shape}")

        if len(x.shape) != 1:
            raise ValueError("x must be a 1-dimensional array")

        self_x = x
        self_x1: NDArray1D
        self_x2: NDArray1D

        if dx is not None:
            if xlo is not None or xhi is not None:
                raise ValueError("dx cannot be used with xlo or xhi")

            if xs is not None:
                raise ValueError("dx cannot be used with xs")

            dx = np.abs(np.atleast_1d(dx))
            dx = cast(NDArray1D, dx)
            if len(dx.shape) != 1:
                raise ValueError("dx must be a 1-dimensional array")
            if x.shape[0] != 1 and dx.shape[0] != 1 and x.shape[0] != dx.shape[0]:
                raise ValueError("dx must have the same shape as x")
            if x.shape[0] == 1 and dx.shape[0] != 1:
                x = np.full(dx.shape, x[0])
                self_x = x

            if dx2 is None:
                self_x1 = x - dx
                self_x2 = x + dx
            else:
                dx2 = np.abs(np.atleast_1d(dx2))
                dx2 = cast(NDArray1D, dx2)
                if len(dx2.shape) != 1:
                    raise ValueError("dx2 must be a 1-dimensional array")
                if x.shape[0] != 1 and dx2.shape[0] != 1 and x.shape[0] != dx2.shape[0]:
                    raise ValueError("dx2 must have the same shape as x")

                self_x1 = x - dx
                self_x2 = x + dx2
        elif dx2 is not None:
            raise ValueError("dx2 cannot be used without dx")
        elif xlo is not None or xhi is not None:
            if xlo is None or xhi is None:
                raise ValueError("xlo and xhi must be used at the same time")

            if xs is not None:
                raise ValueError("xs cannot be used with xlo or xhi")

            xlo = np.atleast_1d(xlo)
            if len(xlo.shape) != 1:
                raise ValueError("xlo must be a 1-dimensional array")
            if xlo.shape[0] != x.shape[0]:
                raise ValueError("xlo must have the same shape as x")

            xhi = np.atleast_1d(xhi)
            if len(xhi.shape) != 1:
                raise ValueError("xhi must be a 1-dimensional array")
            if xhi.shape[0] != x.shape[0]:
                raise ValueError("xhi must have the same shape as x")

            self_x1 = xlo
            self_x2 = xhi
        elif xs is not None:
            xs = np.atleast_1d(xs)
            if len(xs.shape) != 2:
                raise ValueError("xs must be a 2-dimensional array")

            xx = np.stack(xs).T  # type: ignore[call-overload]
            self_x1 = np.min(xx, axis=1)  # type: ignore[no-untyped-call]
            self_x2 = np.max(xx, axis=1)  # type: ignore[no-untyped-call]
        else:
            self_x1 = x
            self_x2 = x

        if self_x.shape != self_x1.shape or self_x.shape != self_x2.shape:
            raise ValueError("central, lower, upper values must have the same shape")

        if np.any((self_x < self_x1) | (self_x2 < self_x)):  # type: ignore[operator]
            raise ValueError("x is out of range [xlo, xhi]")

        object.__setattr__(self, "x", self_x)
        object.__setattr__(self, "x1", self_x1)
        object.__setattr__(self, "x2", self_x2)

    @property
    def dx(self) -> NDArray1D:
        """Return the symmetric errors."""
        x = self.x
        x1 = self.x1
        x2 = self.x2
        return np.max(  # type: ignore[no-any-return, no-untyped-call]
            np.stack((x - x1, x2 - x)).T, axis=1
        )

    @property
    def err(self) -> NDArray2D:
        """Return the lower and upper errors."""
        x = self.x
        x1 = self.x1
        x2 = self.x2
        return np.stack((x - x1, x2 - x))

    @property
    def xlo(self) -> NDArray1D:
        """Return the lower values."""
        return self.x1

    @property
    def xhi(self) -> NDArray1D:
        """Return the upper values."""
        return self.x2

    @property
    def central(self) -> NDArray1D:
        """Return the central value."""
        return self.x

    @property
    def lower(self) -> NDArray1D:
        """Return the lower values."""
        return self.x1

    @property
    def upper(self) -> NDArray1D:
        """Return the upper values."""
        return self.x2

    def __array_ufunc__(
        self, ufunc: np.ufunc, method: str, *args: Any, **kwargs: Any
    ) -> Any:
        """For NumPy ufunc."""
        if len(args) == 2 and len(kwargs) == 0:
            x = args[0]
            y = args[1]
            if isinstance(x, np.ndarray) and isinstance(y, Bounded):
                if ufunc is np.add:
                    return y.__radd__(x)  # type: ignore[operator]
                elif ufunc is np.subtract:
                    return y.__rsub__(x)  # type: ignore[operator]
                elif ufunc is np.multiply:
                    return y.__rmul__(x)  # type: ignore[operator]
                elif ufunc is np.true_divide:
                    return y.__rtruediv__(x)  # type: ignore[operator]
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        """Return ``self ==  other``."""
        if isinstance(other, Bounded):
            return np.all(  # type: ignore [return-value]
                (self.x == other.x) & (self.x1 == other.x1) & (self.x2 == other.x2)
            )
        else:
            return NotImplemented

    def __pos__(self) -> "Bounded":
        """Return ``+ self``."""
        return self

    def __neg__(self) -> "Bounded":
        """Return ``- self``."""
        x = self.x
        x1 = self.x1
        x2 = self.x2

        return Bounded(-x, xs=(-x1, -x2))

    def __add__(self, other: Union["Bounded", int, float, NDArray1D]) -> "Bounded":
        """Return ``self + other``."""
        if isinstance(other, Bounded):
            x = self.x
            x1 = self.x1
            x2 = self.x2
            y = other.x
            y1 = other.x1
            y2 = other.x2
        elif isinstance(other, (int, float, np.ndarray)):
            x = self.x
            x1 = self.x1
            x2 = self.x2
            y = other  # type: ignore[assignment]
            y1 = y
            y2 = y
        else:
            return NotImplemented

        return Bounded(x + y, xlo=x1 + y1, xhi=x2 + y2)

    # NOTE: unfortunately, if we add np.ndarray to the signature of __radd__ etc.,
    # then "unsafely overlapping" happens.

    def __radd__(self, other: Union[int, float]) -> "Bounded":
        """Return ``other + self``."""
        if isinstance(other, (int, float, np.ndarray)):
            x = other
            x1 = x
            x2 = x
            y = self.x
            y1 = self.x1
            y2 = self.x2
        else:
            return NotImplemented  # type: ignore[unreachable]

        return Bounded(x + y, xlo=x1 + y1, xhi=x2 + y2)

    def __sub__(self, other: Union["Bounded", int, float, NDArray1D]) -> "Bounded":
        """Return ``self - other``."""
        if isinstance(other, Bounded):
            x = self.x
            x1 = self.x1
            x2 = self.x2
            y = other.x
            y1 = other.x1
            y2 = other.x2
        elif isinstance(other, (int, float, np.ndarray)):
            x = self.x
            x1 = self.x1
            x2 = self.x2
            y = other  # type: ignore[assignment]
            y1 = y
            y2 = y
        else:
            return NotImplemented

        return Bounded(x - y, xlo=x1 - y2, xhi=x2 - y1)

    def __rsub__(self, other: Union[int, float]) -> "Bounded":
        """Return ``other - self``."""
        if isinstance(other, (int, float, np.ndarray)):
            x = other
            x1 = x
            x2 = x
            y = self.x
            y1 = self.x1
            y2 = self.x2
        else:
            return NotImplemented  # type: ignore[unreachable]

        return Bounded(x - y, xlo=x1 - y2, xhi=x2 - y1)

    def __mul__(self, other: Union["Bounded", int, float, NDArray1D]) -> "Bounded":
        """Return ``self * other``."""
        if isinstance(other, Bounded):
            x = self.x
            x1 = self.x1
            x2 = self.x2
            y = other.x
            y1 = other.x1
            y2 = other.x2

            return Bounded(x * y, xs=(x1 * y1, x1 * y2, x2 * y1, x2 * y2))
        elif isinstance(other, (int, float, np.ndarray)):
            x = self.x
            x1 = self.x1
            x2 = self.x2
            y = other  # type: ignore[assignment]

            return Bounded(x * y, xs=(x1 * y, x2 * y))
        else:
            return NotImplemented

    def __rmul__(self, other: Union[int, float]) -> "Bounded":
        """Return ``other * self``."""
        if isinstance(other, (int, float, np.ndarray)):
            x = other
            y = self.x
            y1 = self.x1
            y2 = self.x2
        else:
            return NotImplemented  # type: ignore[unreachable]

        return Bounded(x * y, xs=(x * y1, x * y2))

    def __truediv__(self, other: Union["Bounded", int, float, NDArray1D]) -> "Bounded":
        """Return ``self / other``."""
        if isinstance(other, Bounded):
            y = other.x
            y1 = other.x1
            y2 = other.x2
            have_zero = (y1 <= 0) & (0 <= y2)  # type: ignore[operator]
            w12 = np.stack((y1 * np.inf, 1 / y1, 1 / y2, y2 * np.inf)).T
            w: NDArray1D = 1 / y
            w1 = np.where(
                have_zero, np.min(w12, axis=1), 1 / y2  # type: ignore[no-untyped-call]
            )
            w2 = np.where(
                have_zero, np.max(w12, axis=1), 1 / y1  # type: ignore[no-untyped-call]
            )
            return self * Bounded(w, xlo=w1, xhi=w2)
        elif isinstance(other, (int, float, np.ndarray)):
            x = self.x
            x1 = self.x1
            x2 = self.x2
            y = other  # type: ignore[assignment]
            return Bounded(x / y, xs=(x1 / y, x2 / y))
        else:
            return NotImplemented

    def __rtruediv__(self, other: Union[int, float]) -> "Bounded":
        """Return ``other / self``."""
        if isinstance(other, (int, float)):
            return Bounded(np.full(self.x.shape, other)) / self
        elif isinstance(other, np.ndarray):  # type: ignore[unreachable]
            return Bounded(other) / self
        else:
            return NotImplemented

    def __pow__(self, other: int) -> "Bounded":
        """Return ``self ** other``."""
        if isinstance(other, int) and other >= 1:
            x = self.x
            x1 = self.x1
            x2 = self.x2
            y = other
            z: NDArray1D = x ** y
            if y % 2 == 0:
                have_zero = (x1 <= 0) & (0 <= x2)  # type: ignore[operator]
                z12 = np.stack((x1 ** y, x2 ** y)).T
                z1 = np.where(
                    have_zero, 0, np.min(z12, axis=1)  # type: ignore[no-untyped-call]
                )
                z2 = np.max(z12, axis=1)  # type: ignore[no-untyped-call]
            else:
                z1 = x1 ** y
                z2 = x2 ** y
            return Bounded(z, xlo=z1, xhi=z2)
        else:
            return NotImplemented
