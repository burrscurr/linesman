What is a straight line?
========================

There are two basic interpretations of what a "straight" line is:

1. A line in a cartesian grid of latitude and longitude (a *loxodrome*)
2. The shortest connection of two points on earth surface (a *geodesic*)

Background
----------
Because the earth is a globe, fitting its surface onto a rectangular shape
(for instance a computer screen) requires stretching out areas towards the poles.
This is called a `mercator projection`_ and is responsible for notable
distortions in the size of various parts of the world (`visualization
<https://thetruesize.com/>`_). A straight line on a
mercator-projected map is called a *loxodrome* or *rhumb line*. Loxodromes
always cross meridians in the same angle.

However, since meridians aren't parallel (at least on the globe), a loxodrome
isn't the shortest path between two points on earth's surface. The acutal
shortest path is called a *geodesic* and is a section of the biggest circle on a
globe (great circle).
See `this website
<https://www8.physics.utoronto.ca/~jharlow/teaching/astrophys03/geodesic.html>`_
for examples.

Relevance
---------

Loxodrome and geodesic don't differ on the equator and meridians, since they
are great circles. However, when moving in other directions, the difference
between a loxodrome and a geodesic between identical points becomes more
important when:

* moving farther to the poles and
* crossing bigger distances.

To find out whether the difference between geodesic and loxodrome is relevant in
context of the expected devatiations of a straight line mission, `this map
<https://academo.org/demos/geodesics/>`_ might be helpful.

Linesman's understanding of a straight line
-------------------------------------------

By default, linesman always uses a geodesic as reference line. Using a loxodrome
as reference line might be implemented in a future release.

.. _mercator projection: https://en.wikipedia.org/wiki/Mercator_projection
