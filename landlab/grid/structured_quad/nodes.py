import itertools

import numpy as np

from ..base import CORE_NODE, FIXED_VALUE_BOUNDARY


def number_of_nodes(shape):
    """Number of nodes is a structured quad grid.

    Parameters
    ----------
    shape : tuple of int
        Shape of grid of nodes.

    Returns
    -------
    int :
        Number of nodes in the grid.

    Examples
    --------
    >>> from landlab.grid.structured_quad.nodes import number_of_nodes
    >>> number_of_nodes((3, 4))
    12
    """
    return np.prod(shape)


def number_of_core_nodes(shape):
    """Number of core nodes is a structured quad grid.

    Parameters
    ----------
    shape : tuple of int
        Shape of grid of nodes.

    Returns
    -------
    int :
        Number of core nodes in the grid.

    Examples
    --------
    >>> from landlab.grid.structured_quad.nodes import number_of_core_nodes
    >>> number_of_core_nodes((3, 4))
    2
    """
    return np.prod(np.array(shape) - 2)


def corners(shape):
    """IDs of corner nodes.

    Parameters
    ----------
    shape : tuple of int
        Shape of grid of nodes.

    Returns
    -------
    (4, ) ndarray :
        IDs of the corner nodes.

    Examples
    --------
    >>> from landlab.grid.structured_quad.nodes import corners
    >>> corners((3, 4))
    array([ 0,  3,  8, 11])
    """
    node_count = number_of_nodes(shape)
    return np.array([0, shape[1] - 1, node_count - shape[1], node_count - 1])


def node_ids(shape):
    """IDs of nodes.

    Parameters
    ----------
    shape : tuple of int
        Shape of grid of nodes.

    Returns
    -------
    ndarray :
        IDs of the nodes.

    Examples
    --------
    >>> from landlab.grid.structured_quad.nodes import node_ids
    >>> node_ids((3, 4))
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]])
    """
    return np.arange(number_of_nodes(shape)).reshape(shape)


def interior_nodes(shape):
    """IDs of interior nodes.

    Parameters
    ----------
    shape : tuple of int
        Shape of grid of nodes.

    Returns
    -------
    (M, N) ndarray :
        IDs of the interior nodes.

    Examples
    --------
    >>> from landlab.grid.structured_quad.nodes import interior_nodes
    >>> interior_nodes((3, 4))
    array([[5, 6]])
    >>> interior_nodes((4, 5))
    array([[ 6,  7,  8],
           [11, 12, 13]])
    """
    node_ids = np.arange(number_of_nodes(shape)).reshape(shape)
    return node_ids[1:-1, 1:-1]


def top_iter(shape):
    """Iterator for the top perimeter nodes.
    """
    return xrange(shape[1] * (shape[0] - 1), shape[0] * shape[1])


def bottom_iter(shape):
    """Iterator for the bottom perimeter nodes.
    """
    return xrange(0, shape[1])


def left_iter(shape):
    """Iterator for the left perimeter nodes.
    """
    return xrange(0, shape[0] * shape[1], shape[1])


def right_iter(shape):
    """Iterator for the right perimeter nodes.
    """
    return xrange(shape[1] - 1, shape[0] * shape[1], shape[1])


def left_right_iter(shape, *args):
    """Iterator for left and right perimeter nodes.

    Examples
    --------
    >>> import numpy as np
    >>> from landlab.grid.structured_quad.nodes import left_right_iter
    >>> np.fromiter(left_right_iter((4, 3)), dtype=np.int)
    array([ 0,  2,  3,  5,  6,  8,  9, 11])
    >>> np.fromiter(left_right_iter((4, 3), 2), dtype=np.int)
    array([0, 2, 3, 5])
    >>> np.fromiter(left_right_iter((4, 3), 2, 4), dtype=np.int)
    array([ 6,  8,  9, 11])
    >>> np.fromiter(left_right_iter((4, 3), 1, 4, 2), dtype=np.int)
    array([ 3,  5,  9, 11])
    """
    if len(args) == 0:
        iter_rows = xrange(0, shape[0], 1)
    elif len(args) == 1:
        iter_rows = xrange(0, args[0], 1)
    elif len(args) == 2:
        iter_rows = xrange(args[0], args[1], 1)
    elif len(args) == 3:
        iter_rows = xrange(args[0], args[1], args[2])

    for row in iter_rows:
        yield row * shape[1]
        yield row * shape[1] + shape[1] - 1


def bottom_top_iter(shape):
    """Iterator for the bottom and top perimeter nodes.

    Examples
    --------
    >>> import numpy as np
    >>> from landlab.grid.structured_quad.nodes import bottom_top_iter
    >>> np.fromiter(bottom_top_iter((4, 3)), dtype=np.int)
    array([ 0,  1,  2,  9, 10, 11])
    """
    return itertools.chain(bottom_iter(shape), top_iter(shape))


def perimeter_iter(shape):
    """Iterator for all perimeter nodes.

    Examples
    --------
    >>> import numpy as np
    >>> from landlab.grid.structured_quad.nodes import perimeter_iter
    >>> np.fromiter(perimeter_iter((4, 3)), dtype=np.int)
    array([ 0,  1,  2,  3,  5,  6,  8,  9, 10, 11])
    """
    return itertools.chain(bottom_iter(shape),
                           left_right_iter(shape, 1, shape[0] - 1),
                           top_iter(shape))


def perimeter(shape):
    """Perimeter nodes.

    Parameters
    ----------
    shape : tuple of int
        Shape of grid of nodes.

    Returns
    -------
    ndarray :
        IDs of the perimeter nodes.

    Examples
    --------
    >>> from landlab.grid.structured_quad.nodes import perimeter
    >>> perimeter((3, 4))
    array([ 0,  1,  2,  3,  4,  7,  8,  9, 10, 11])

    """
    return np.fromiter(perimeter_iter(shape), dtype=np.int)


def status_with_perimeter_as_boundary(shape, status_on_perimeter=FIXED_VALUE_BOUNDARY):
    """Node status for a grid whose boundary is along its perimeter.

    Parameters
    ----------
    shape : tuple of int
        Shape of grid of nodes.

    Returns
    -------
    ndarray :
        Node status for grid.

    Examples
    --------
    >>> from landlab.grid.structured_quad.nodes import status_with_perimeter_as_boundary
    >>> status_with_perimeter_as_boundary((3, 4))
    array([[1, 1, 1, 1],
           [1, 0, 0, 1],
           [1, 1, 1, 1]])
    >>> status_with_perimeter_as_boundary((3, 4), status_on_perimeter=-1)
    array([[-1, -1, -1, -1],
           [-1,  0,  0, -1],
           [-1, -1, -1, -1]])
    """
    status = np.empty(shape, dtype=int)
    status.fill(CORE_NODE)
    status.flat[perimeter(shape)] = status_on_perimeter

    return status
