""":mod:`battlib.utilities` contains various tools."""

import numpy as np


def intexterp(x, xp, fp):
    """Interpolate/extrapolate the value.

    :param x: The value to interpolate/extrapolate.
    :param xp: The values to interpolate/extrapolate.
    :param fp: The values to be interpolated/extrapolated.
    :return: The interpolated/extrapolated value.
    """
    if x < xp[0]:
        value = fp[0] + (fp[1] - fp[0]) / (xp[1] - xp[0]) * (x - xp[0])
    elif xp[-1] < x:
        value = fp[-1] + (fp[-1] - fp[-2]) / (xp[-1] - xp[-2]) * (x - xp[-1])
    else:
        value = np.interp(x, xp, fp)

    return value
