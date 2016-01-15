# Livewire
This repository contains a working implementation of Livewire algorithm for image segmentation. The notebook includes a script that loads a demo DICOM image (MR head scan), and allows the user to segment a structure in the brain by setting seed points and letting Livewire algorithm compute the shortest path to the next seed point. The algorithm suggestions are displayed as user moves the mouse over the image.

## Technical requirements
To run this script, you will need:
- [ipython](http://ipython.org) (for Python 2.7)
- ipython notebooks, aka [Jupyter notebooks](http://jupyter.org)
- [scikit-image](http://scikit-image.org)
- [matplotlib](http://matplotlib.org)
You can get them all out-of-the-box in an [Anaconda install](https://www.continuum.io/downloads).

## Screenshot
![Livewire example](screenshot.png)
