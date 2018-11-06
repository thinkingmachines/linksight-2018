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

DatasetMatchingTask
===================

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.matching
   :noindex:

.. java:type:: public class DatasetMatchingTask

Fields
------
matchingStats
^^^^^^^^^^^^^

.. java:field:: public final MatchingStats matchingStats
   :outertype: DatasetMatchingTask

Constructors
------------
DatasetMatchingTask
^^^^^^^^^^^^^^^^^^^

.. java:constructor:: public DatasetMatchingTask(InputSource inputSource, OutputSink outputSink, Executor executor, AddressMatcher addressMatcher, MatchesType matchesType)
   :outertype: DatasetMatchingTask

Methods
-------
run
^^^

.. java:method:: public void run() throws Throwable
   :outertype: DatasetMatchingTask

run
^^^

.. java:method:: public void run(boolean verbose) throws Throwable
   :outertype: DatasetMatchingTask

