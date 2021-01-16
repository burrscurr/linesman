Evaluating the track
========================

Reading the gpx file
--------------------

A gpx file can contain multiple tracks with recorded track points. Linesman always
selects the first track, even if there are multiple tracks.

Evaluating the track
--------------------

Linesman compares every point of the selected track to the reference line.
In general, that comparision is the shortest distance of the point to the
reference line. The list of these distances is then aggregated further, e.g. to
calculate average or maximum.

.. note::
  Since linesman does not consider the distance of between track points,
  sections with many points may be overrepresented compared to sections with low
  track point density.

  It is planned to adjust this in a future release by resampling the recorded
  line from equidistant points from the reference line.
