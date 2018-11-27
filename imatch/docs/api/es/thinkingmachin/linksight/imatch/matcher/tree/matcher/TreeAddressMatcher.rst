.. java:import:: com.google.common.collect Ordering

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Util

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset TestDataset

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor Executor

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor SeriesExecutor

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.sink ListSink

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.source CsvSource

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.matching AddressMatcher

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.matching DatasetMatchingTask

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.model FuzzyStringMap

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.reference ReferenceMatch

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.tree AddressTreeNode

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.tree TreeReference

.. java:import:: io.reactivex.annotations NonNull

.. java:import:: org.apache.commons.math3.util Pair

.. java:import:: java.util.stream Collectors

TreeAddressMatcher
==================

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.tree.matcher
   :noindex:

.. java:type:: public class TreeAddressMatcher implements AddressMatcher

   This class performs the matching algorithm to the reference tree.

Constructors
------------
TreeAddressMatcher
^^^^^^^^^^^^^^^^^^

.. java:constructor:: public TreeAddressMatcher(TreeReference reference)
   :outertype: TreeAddressMatcher

Methods
-------
getTopMatches
^^^^^^^^^^^^^

.. java:method:: @NonNull @Override public List<ReferenceMatch> getTopMatches(Address address, int numMatches)
   :outertype: TreeAddressMatcher

   Gets the top matches returned by the matching algorithm

   :param address: the address to be processed
   :param numMatches: the number of matches to be used
   :return: a list of the top N matches

