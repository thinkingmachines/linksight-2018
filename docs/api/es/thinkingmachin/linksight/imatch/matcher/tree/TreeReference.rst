.. java:import:: com.google.common.base Stopwatch

.. java:import:: com.google.common.collect HashMultimap

.. java:import:: com.google.common.collect Ordering

.. java:import:: de.siegmar.fastcsv.reader CsvParser

.. java:import:: de.siegmar.fastcsv.reader CsvRow

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Psgc

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Util

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset PsgcDataset

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset TestDataset

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor Executor

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor ParallelExecutor

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor SeriesExecutor

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.sink ListSink

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.source CsvSource

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.matching DatasetMatchingTask

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.model FuzzyStringMap

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.reference PsgcRow

.. java:import:: org.apache.commons.collections4.multiset HashMultiSet

.. java:import:: org.apache.commons.math3.util Pair

.. java:import:: java.io IOException

.. java:import:: java.util Comparator

.. java:import:: java.util HashMap

.. java:import:: java.util List

.. java:import:: java.util Set

.. java:import:: java.util.concurrent TimeUnit

.. java:import:: java.util.stream Collectors

TreeReference
=============

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.tree
   :noindex:

.. java:type:: public class TreeReference

Fields
------
DEFAULT_PSGC_DATASET
^^^^^^^^^^^^^^^^^^^^

.. java:field:: public static PsgcDataset DEFAULT_PSGC_DATASET
   :outertype: TreeReference

EXTRA_PSGC_DATASET
^^^^^^^^^^^^^^^^^^

.. java:field:: public static PsgcDataset EXTRA_PSGC_DATASET
   :outertype: TreeReference

entryPoint
^^^^^^^^^^

.. java:field:: public final AddressTreeNode entryPoint
   :outertype: TreeReference

root
^^^^

.. java:field:: public final AddressTreeNode root
   :outertype: TreeReference

Constructors
------------
TreeReference
^^^^^^^^^^^^^

.. java:constructor:: public TreeReference(PsgcDataset[] psgcDatasets) throws IOException
   :outertype: TreeReference

