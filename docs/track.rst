Evaluating the track
====================

Reading the gpx file
--------------------

A gpx file can contain multiple tracks with recorded track points. Linesman always
selects the first track, even if there are multiple tracks.

Transforming the coordinate system
----------------------------------

To simplify further calculations, the points from the track are transformed into
a cartesian grid with grid size 1 Meter. This is achieved using an `oblique
mercator projection <https://en.wikipedia.org/wiki/Oblique_Mercator_projection>`_,
which creates a new coordinate system in which the reference line becomes the
x-Axis and deviations from the reference line are measured in direction of the
y-Axis. Therfore, the deviation of a point is expressed in its y coordinate,
which makes further calculations much easier.

Since the deviations from the straight line are expected to be small, the
oblique mercator transformation has great accuracy – similar to the regular
mercator, which has good distance accuracy in proximity to the equator.

.. note::
  Since the distance between recorded GPS points depend on the frequency of
  measurements and movement velocity, there may be over- and underrepresented
  sections in a recorded track. This is reflected in the transformed cartesian grid,
  where the x coordinates of the transformed points must not be equidistant.

  While this does not affect quality measures like maximum deviation, other
  measures like an average can be skewed. It is planned to adjust for density
  of measurements in a future release, e.g.
  by resampling the recorded line from equidistant points on the reference line.

Calculating quality measures
------------------------------

After transformation, the deviation of a point to the reference line is equal to
its y coordinate, such that calculating quality measures like the devation
maximum becomes very simple.
