.. Livewire Segmentation documentation master file, created by
   sphinx-quickstart on Wed Jan 27 08:16:20 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Livewire Segmentation's documentation!
=================================================

Contents:

.. toctree::
   :maxdepth: 2

This package implements Livewire segmentation algorithm for image segmentation.
The general idea of the algorithm is to use image information for segmentation and avoid crossing
object boundaries. A gradient image highlights the boundaries, and Dijkstra's shrotest path
algorithm computes a path using gradient differences as segment costs.
Thus the line avoids strong gradients in the gradient image, which corresponds to following object boundaries
in the original image.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

