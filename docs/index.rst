Livewire Segmentation Algorithm
===============================

Contents:

.. toctree::
   :maxdepth: 2

This package implements
`Livewire segmentation algorithm <https://en.wikipedia.org/wiki/Livewire_Segmentation_Technique>`_
for image segmentation aka `intelligent scissors`.
The general idea of the algorithm is to use image information for segmentation and avoid crossing
object boundaries. A `gradient image <https://en.wikipedia.org/wiki/Image_gradient>`_ highlights the boundaries,
and `Dijkstra's shortest path <https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm>`_
algorithm computes a path using gradient differences as segment costs.
Thus the line avoids strong gradients in the gradient image, which corresponds to following object boundaries
in the original image.

How to use
==========

The package is easy to use. First, read/import/generate an image:

.. code:: python

    from skimage import data
    image = data.coins()

Then compute the shortest path. The short version:

.. code:: python

    from livewire import compute_shortest_path
    path_standalone = compute_shortest_path(image, (0, 0), (10, 25))

or a longer version:

.. code:: python

    from livewire import LiveWireSegmentation
    algorithm = LiveWireSegmentation(image)
    path = algorithm.compute_shortest_path((0, 0), (10, 25))

Installation
============

This package is hosted at `github`_.
You can clone it, or download a zipped version of source code.

Requirements
------------

This package requires `scikit-image <http://scikit-image.org>`_ of version at least `0.11.3`.

Contribute
==========

If you think you can contribute to this project, simply fork it on `github`_,
then publish a pull request when you are done.

Support
=======

If yu are having issues with this code, let me know. You can create an issue on `github`_. I will get back to you.

License
=======

The project is licensed under the BSD license.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _`github`:  https://github.com/pdyban/livewire
