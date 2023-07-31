.. _quickstart:

Quick Start
============


Installing astroQTpy
++++++++++++++++++++

Install ``astroqtpy`` using ``pip``:

.. code-block:: bash
	
	$ pip install astroqtpy

(See the :ref:`installation` page.)


Getting started
+++++++++++++++

Importing the quadtree module
-----------------------------

This is the main module in ``astroqtpy``, which contains various quadtree classes for
different purposes.

In a Python script or Jupyter notebook:

.. code-block:: python
	
	import astroqtpy.quadtree as qt

This should be all you need for most simple applications. 

If you wish to define your own quadtree class 
with ``astroqtpy``, you will need to import additional modules:

.. code-block:: python
	
	from astroqtpy.basetree import BaseTree
	from astroqtpy.quadnode import QuadNode
	from astroqtpy.quadpoint import QuadPoint


Instantiating a quadtree class
------------------------------

Once you've imported the quadtree module (or defined your own quadtree class),
you must create an instance of a quadtree class. For example:

.. code-block:: python
	
	my_random_quadtree = qt.RandomQuadTree(0, 1, 0, 1)

For the ``RandomQuadTree`` class, at minimum you must specificy the lower and 
upper x and y limits for the quadtree. For a description of all optional arguments
and other quadtree classes, please see the :ref:`api`.


Running a quadtree
------------------

Each quadtree class has two methods that you are most likely 
to use: `run_quadtree()` and `draw_tree()`. As the names imply,
these methods act to run the quadtree algorithm forward, and 
plot the quadtree on a Matplotlib axis.

.. code-block:: python
	
	my_random_quadtree.run_quadtree()

.. code-block:: python
	
	import matplotlib.pyplot as plt
	
	fig, ax = plt.subplots()
	my_random_quadtree.draw_tree(ax)


Learn more
++++++++++

To learn more, continue on to the :ref:`tutorials` and check out
the :ref:`api`.

.. image:: img/astroQTpy_logo_justpie_withborder.png
   :width: 20%
   :align: center