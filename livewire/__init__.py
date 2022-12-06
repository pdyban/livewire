from .livewiresegmentation import LiveWireSegmentation
from .trackmanager import Trackmanager


def compute_shortest_path(image, from_, to_, length_penalty=0.0):
    """
    Inline function for easier computation of shortest_path in an image.

    This function will
    create a new instance of LiveWireSegmentation class every time
    it is called, calling for a recomputation of the gradient image and
    the shortest path graph.
    If you need to compute the shortest path in one image more than once,
    use the class-form initialization instead.

    :param image: image on which the shortest path should be computed
    :type image: 2D numpy array
    :param from_: starting point for path computation
    :type from_: tuple with 2 elements (x, y)
    :param to_: target point for path computation
    :type to_: tuple with 2 elements (x, y)
    :param length_penalty: coefficient for penalizing long paths
    :return: shortest path as a list of tuples (x, y), including from_ and to_
    """
    algorithm = LiveWireSegmentation(image)
    return algorithm.compute_shortest_path(from_, to_, length_penalty=length_penalty)
