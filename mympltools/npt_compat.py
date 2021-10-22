"""Compatibility helpers for NumPy Typing."""

from typing import TYPE_CHECKING, Any

__all__ = ("ArrayLike", "NDArray1D", "NDArray2D")

if TYPE_CHECKING:
    from numpy.typing import ArrayLike as npt_ArrayLike
    from numpy.typing import NDArray as npt_NDArray

    ArrayLike = npt_ArrayLike
    NDArray1D = npt_NDArray[Any]
    NDArray2D = npt_NDArray[Any]
else:
    ArrayLike = Any
    NDArray1D = Any
    NDArray2D = Any
