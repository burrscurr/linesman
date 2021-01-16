linesman documentation
======================

linesman is a command line tool calculating quality measures evaluating the
straightness of a GPS track.

Getting Started
---------------

linesman is a python package and can be installed with pip:

.. code:: console

  pip install gpx-linesman

For usage information, use linesman's built-in help:

.. code:: console

  linesman --help

linesman development is coordinated via `github`_. Feel free to submit bugs,
feature requests and to contribute to the source code.

Motivation
----------

linesman is inspired by `geowizard`_, a youtuber who popularized crossing
areas in a completely straight line. While overcoming natural and/or man-made
obstacles, one attempts sticking as closely as possible to the straight,
predefined line.

Commonly, a straight line mission is judged by the maximum deviation from the
reference line. Especially with longer straight line missions, determining the
biggest deviation can become a cumbersome task. Also, line quality measures
requiring to evaluate every point of the GPS track (for instance the average
deviation) are practically impossible to calculate by hand.

That's where linesman comes in: It parses the recorded line from a gpx file and
allows users to choose from a variety of line quality measures to calculate.

Scope of this documentation
------------------------------

This documentation mainly focuses on central concepts of linesman. For
user-oriented documentation, use the built-in help.

.. toctree::
  :caption: Concepts
  :maxdepth: 1

  straightness
  track

.. _geowizard: https://www.youtube.com/c/GeoWizard
.. _github: https://github.com/burrscurr/linesman
