.. java:import:: com.google.common.base Stopwatch

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.sink OutputSink

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.source InputSource

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor Executor

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.reference ReferenceMatch

.. java:import:: java.io IOException

.. java:import:: java.io UncheckedIOException

.. java:import:: java.util List

.. java:import:: java.util.concurrent TimeUnit

.. java:import:: java.util.concurrent.atomic AtomicInteger

DatasetMatchingTask.MatchesType
===============================

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.matching
   :noindex:

.. java:type:: public enum MatchesType
   :outertype: DatasetMatchingTask

   Count of top matches that can be used.

Enum Constants
--------------
MULTIPLE
^^^^^^^^

.. java:field:: public static final DatasetMatchingTask.MatchesType MULTIPLE
   :outertype: DatasetMatchingTask.MatchesType

SINGLE
^^^^^^

.. java:field:: public static final DatasetMatchingTask.MatchesType SINGLE
   :outertype: DatasetMatchingTask.MatchesType

Fields
------
numMatches
^^^^^^^^^^

.. java:field:: public int numMatches
   :outertype: DatasetMatchingTask.MatchesType

