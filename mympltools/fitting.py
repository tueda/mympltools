"""Fitting routines."""

import dataclasses
from typing import Callable, Generic, TypeVar

import numpy as np

from .npt_compat import ArrayLike, NDArray1D, NDArray2D

T = TypeVar("T")


@dataclasses.dataclass(frozen=True, repr=True)
class Model(Generic[T]):
    """Fitted model."""

    f: Callable[..., T]
    popt: NDArray1D
    perr: NDArray1D
    pcov: NDArray2D
    chi2: float
    ndf: int
    p_value: float

    def __call__(self, x: T) -> T:
        """Perform interpolation/extrapolation."""
        return self.f(x, *self.popt)


def fit(
    f: Callable[..., T], xdata: ArrayLike, ydata: ArrayLike, yerr: ArrayLike
) -> Model[T]:
    """Fit a function to data."""
    import scipy.optimize
    import scipy.stats.distributions

    xdata = np.atleast_1d(xdata)
    ydata = np.atleast_1d(ydata)
    yerr = np.atleast_1d(yerr)

    popt, pcov = scipy.optimize.curve_fit(
        f, xdata, ydata, sigma=yerr, absolute_sigma=True
    )
    perr = np.sqrt(np.diag(pcov))
    chi2 = np.sum(((f(xdata, *popt) - ydata) / yerr) ** 2)
    ndf = len(xdata) - len(popt)
    p_value = scipy.stats.distributions.chi2.sf(chi2, ndf)

    return Model(f, popt, perr, pcov, chi2, ndf, p_value)
