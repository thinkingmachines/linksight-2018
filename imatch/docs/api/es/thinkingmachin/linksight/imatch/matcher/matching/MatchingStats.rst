.. java:import:: es.thinkingmachin.linksight.imatch.matcher.reference ReferenceMatch

.. java:import:: java.util.concurrent.atomic AtomicInteger

.. java:import:: java.util.concurrent.atomic LongAccumulator

.. java:import:: java.util.concurrent.atomic LongAdder

MatchingStats
=============

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.matching
   :noindex:

.. java:type:: public class MatchingStats

   This class sets the benchmark statistics for the results of the matching algorithm. It categorizes the match based on benchmark values and counts the total number of matches under a certain benchmark.

Fields
------
brgyLevelCount
^^^^^^^^^^^^^^

.. java:field:: public final LongAdder brgyLevelCount
   :outertype: MatchingStats

nullCount
^^^^^^^^^

.. java:field:: public final LongAdder nullCount
   :outertype: MatchingStats

score075Count
^^^^^^^^^^^^^

.. java:field:: public final LongAdder score075Count
   :outertype: MatchingStats

score095Count
^^^^^^^^^^^^^

.. java:field:: public final LongAdder score095Count
   :outertype: MatchingStats

score100Count
^^^^^^^^^^^^^

.. java:field:: public final LongAdder score100Count
   :outertype: MatchingStats

totalCount
^^^^^^^^^^

.. java:field:: public final LongAdder totalCount
   :outertype: MatchingStats

Methods
-------
addNewMatch
^^^^^^^^^^^

.. java:method:: public void addNewMatch(ReferenceMatch match)
   :outertype: MatchingStats

   Categorizes the match based on its score and increments the corresponding benchmark.

   :param match: the matched value

printStats
^^^^^^^^^^

.. java:method:: public void printStats()
   :outertype: MatchingStats

   Prints the benchmarking statistics

