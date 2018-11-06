.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset Dataset

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.sink LinkSightCsvSink

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.source CsvSource

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.matching AddressMatcher

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.matching DatasetMatchingTask

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor SeriesExecutor

.. java:import:: es.thinkingmachin.linksight.imatch.server.messaging Response

LinkSightCsvMatchingJob
=======================

.. java:package:: es.thinkingmachin.linksight.imatch.server.jobs
   :noindex:

.. java:type:: public class LinkSightCsvMatchingJob extends Job

Fields
------
addressMatcher
^^^^^^^^^^^^^^

.. java:field:: protected AddressMatcher addressMatcher
   :outertype: LinkSightCsvMatchingJob

dataset
^^^^^^^

.. java:field:: protected Dataset dataset
   :outertype: LinkSightCsvMatchingJob

Constructors
------------
LinkSightCsvMatchingJob
^^^^^^^^^^^^^^^^^^^^^^^

.. java:constructor:: public LinkSightCsvMatchingJob(String id, AddressMatcher addressMatcher, Dataset dataset)
   :outertype: LinkSightCsvMatchingJob

Methods
-------
run
^^^

.. java:method:: @Override public Response run()
   :outertype: LinkSightCsvMatchingJob

