.. _home:

.. image:: img/astroQTpy_logo_withtext.png
   :width: 60%
   :align: center
   :alt: astroQTpy logo

.. raw:: html

   <h1 align="center">Efficient 2D mapping for astronomers</h1>

   <hr>

   <p align="center">
      <a href='https://astroqtpy.readthedocs.io/en/latest/?badge=latest' >
         <img src='https://readthedocs.org/projects/astroqtpy/badge/?version=latest' alt='Documentation Status' />
      </a>
      <a href="https://pypi.org/project/astroQTpy/">
         <img alt="PyPi" src="https://img.shields.io/pypi/v/astroQTpy">
      </a>
      <a href="https://zenodo.org/badge/latestdoi/666798611">
         <img src="https://zenodo.org/badge/666798611.svg" alt="DOI">
      </a>
      <a href="https://github.com/CalebHarada/astroQTpy/blob/main/LICENSE">
         <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License">
      </a>
      <a href="https://github.com/CalebHarada/astroQTpy/tree/main">
         <img alt="GitHub" src="https://img.shields.io/badge/github-main-purple">
      </a>
   </p>

   <p align="center">
      Hello! Welcome to the documentation for <code style="color:red">astroQTpy</code> (Astronomy Quad Trees in Python), 
      a Python package for efficiently mapping 2D parameter space using quadtrees.
   </p>

   <br />


What is astroQTpy?
------------------

``astroQTpy`` makes it easy to implement `quadtree <https://en.wikipedia.org/wiki/Quadtree#:~:text=A%20quadtree%20is%20a%20tree,into%20four%20quadrants%20or%20regions.>`_ 
data structures in your astronomical research. Quadtrees are an efficient way to partition a two-dimensional space by recursively subdividing it into 
four equal quadrants (or nodes). 

In practice, this can speed up your simulations or data analysis by focusing your computational resources on regions of parameter space where large 
gradients or inhomogeneities exist. In other words, you don't have to waste time computing models where you know large areas of your parameter 
space yield similar results because ``astroQTpy`` quadtrees automatically subdivide where inhomogeneities exist. You can also use ``astroQTpy`` to
simply create 2D histograms of your data. 

As an added bonus, quadtrees look really cool when you plot them. Nice!

.. image:: img/linear_chi2_tutorial_quadtree.png
   :width: 45%
   :alt: Example of a chi-squared quadtree
.. image:: img/nbody_megno_tutorial_quadtree.png
   :width: 45%
   :alt: Example of an N-body stability map quadtree

To get started using ``astroQTpy``, check out the :ref:`quickstart` guide or follow along with the :ref:`tutorials`.

.. Note::
   
   ``astroQTpy`` is a living project that will be continually updated and upgraded over time. Check back for updates 
   or feel free to give us suggestions by `creating a new issue on GitHub <https://github.com/CalebHarada/astroQTpy/issues>`_. 
   You can also define your own custom ``astroQTpy`` class -- check out the tutorials for more info!


Why use quadtrees?
------------------

There are many potential applications of quadtrees in astronomical research! In general, quadtrees can be useful just about anywhere 
you need to plot some values as a function of two independent variables. 

Just to name a few examples where you might use a quadtree:

* Grid-based approach to model optimization.

   - E.g., plotting :math:`\chi^2` as a function of two model parameters.

* N-body simulation grids.

   - E.g., MEGNO as a function of two orbital elements.

* Pipeline sensitivity maps.

   - E.g., Exoplanet transit injection/recovery tests as a function of :math:`R_p/R_*` and period.

* 2D histograms.

   - E.g., H-R Diagram for a large number of stars.

.. image:: img/quadtree_animation.gif
   :width: 60%
   :align: center
   :alt: GIF animation showing the progression of an N-body quadtree


Attribution:
++++++++++++

* If you use ``astroQTpy`` in your work, please cite our `Zenodo <https://zenodo.org/record/8187916>`_:

.. code-block:: TeX

   @software{harada_astroQTpy_2023,
      author       = {Caleb K. Harada},
      title        = {astroQTpy},
      month        = jul,
      year         = 2023,
      publisher    = {Zenodo},
      version      = {latest},
      doi          = {10.5281/zenodo.8187916},
      url          = {https://doi.org/10.5281/zenodo.8187916}
   }

* If you use `REBOUND <https://rebound.readthedocs.io/en/latest/>`_ or any of dependencies,
  please also cite those. The simplest way to find the citations relevant to the specific setup of your ``REBOUND`` simulation is:

.. code-block:: python

   sim = rebound.Simulation()
   -your setup-
   sim.cite()


.. Note::

   The backbone of ``astroQTpy`` is based upon the quadtree algorithm described
   by `Ment & Charbonneau (2023) <https://ui.adsabs.harvard.edu/abs/2023AJ....165..265M/abstract>`_.
   We thank the authors for their insight and helpful discussions about quadtrees.


User Guide:
+++++++++++

.. toctree::
   :maxdepth: 2

   quickstart
   installation
   tutorials
   api

Changelog:
++++++++++

**0.2.0 (2023-08-17)**

- Clean up 2D histogram feature, complete docs and tutorials (@CalebHarada)

**0.1.7 (2023-08-16)**

- Add 2D histogram feature (@CalebHarada)

**0.1.6 (2023-08-16)**

- Add overwrite option (@CalebHarada)

**0.1.5 (2023-08-03)**

- Minor bug fixes, update docs (@CalebHarada)

**0.1.4 (2023-07-31)**

- Complete documentation (@CalebHarada)

**0.1.3 (2023-07-28)**

- New tutorials, update docs, etc. (@CalebHarada)

**0.1.2 (2023-07-27)**

- Update docs, etc. (@CalebHarada)

**0.1.1 (2023-07-26)**

- First release on Zenodo (@CalebHarada)

   

