"""
    File that contains several utility functions to calculate properties of
    molecules.
"""

# ##############################################################################
# Imports
# ##############################################################################

# General.
import numpy

from numpy import ndarray, float64
from typing import Any

# ##############################################################################
# Functions
# ##############################################################################

# ------------------------------------------------------------------------------
# Get Functions
# ------------------------------------------------------------------------------


def get_center_of_diffusion(dtensor: ndarray) -> ndarray:
    """
        From the 6x6 diffusion tensor, gets the location of the center of
        diffusion.

        :param dtensor: The 6x6 diffusion tensor.

        :return: The 3D array that represents the center of diffusion.
    """

    # Get the appropriate tensors.
    rr = dtensor[3:, 3:]
    tr = dtensor[3:, :3]

    # Matrix with rotation-rotation coupling.
    matrix = numpy.linalg.inv(numpy.array(
         [
             [rr[1, 1] + rr[2, 2], -rr[0, 1], -rr[0, 2]],
             [-rr[0, 1], rr[0, 0] + rr[2, 2], -rr[1, 2]],
             [-rr[0, 2], -rr[1, 2], rr[0, 0] + rr[1, 1]]
         ], dtype=float64
    ))

    # The vector with the assymetric translation-rotation entries.
    vector = numpy.array(
        [
            [tr[1, 2] - tr[2, 1]],
            [tr[2, 0] - tr[0, 2]],
            [tr[0, 1] - tr[1, 0]]
        ], dtype=float64
    )

    return numpy.transpose(numpy.matmul(matrix, vector))[0]


def get_center_of_geometry(coordinates: ndarray, radii: ndarray) -> ndarray:
    """
        From the given set of coordinates and the radius array, gets the center
        of geometry of the molecule.

        :param coordinates: The coordinates of the atoms in the molecule.

        :param radii: The radii of the atoms in the molecule.

        :return: The average of the maximum and minimum coordinates in the
         system.
    """

    # Get the maximum.
    maximum = numpy.array(
        [crd + rds for crd, rds in zip(coordinates, radii)],
        dtype=float64
     )
    maximum = numpy.array(
        [max(maximum[:, i]) for i in range(3)],
        dtype=float64
     )

    # Get the maximum.
    minimum = numpy.array(
        [crd - rds for crd, rds in zip(coordinates, radii)],
        dtype=float64
    )
    minimum = numpy.array(
        [min(minimum[:, i]) for i in range(3)],
        dtype=float64
    )

    return (maximum + minimum) * 0.5


def get_center_of_mass(coordinates: ndarray, masses: ndarray) -> ndarray:
    """
        From the given set of coordinates and the mass array, gets the center of
        mass of the molecule.

        :param coordinates: The coordinates of the atoms in the molecule.

        :param masses: The masses of the atoms in the molecule.

        :return: The coordinate average, weighted by the masses in the system.
    """

    # Get the dot product.
    com = numpy.dot(masses, coordinates)

    return com / numpy.sum(masses)


# ------------------------------------------------------------------------------
# Validate Functions
# ------------------------------------------------------------------------------


def validate_array(array: Any, dims: int = 3, exception: bool = False) -> bool:
    """
        Validates if the given array is a numpy array of the given dimensions,
        with float64 as the type of element.

        :param array: The object to be validated.

        :param dims: The number of dimensions the array must have.

        :param exception: If an exception must be raised if the validation
         fails.

        :raise ValueError: If the array has the wrong number of dimensions.

        :raise TypeError: If the array is NOT a numpy array or the type of
         values in the array are the wrong type.
    """

    # Determine if the array is a numpy array.
    valid = isinstance(array, (ndarray,))
    if not valid and exception:
        raise TypeError(
            "The object is not a numpy array, the object is of type: "
            f"{type(array)}."
        )

    # Determine if the array has the proper dimensions.
    valid = valid and len(array) == dims
    if not valid and exception:
        raise ValueError(
            f"The object is a numpy array with the wrong length, it must be "
            f"{dims}. The array currently has {len(array)} entries and the "
            f"entries are {array}."
        )

    # Determine if the array values have the proper type.
    valid = valid and all(map(lambda x: type(x) == float64, array))
    if not valid and exception:
        raise ValueError(
            "The object is a numpy array with the right length, but with the "
            f"wrong type of entries, that must be {float64}, the entry types "
            f"are currently {tuple(map(type, array))}."
        )

    return valid