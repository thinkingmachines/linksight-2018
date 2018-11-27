.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset Dataset

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset TestDataset

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.eval Evaluator

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor Executor

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor ParallelExecutor

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.sink LinkSightCsvSink

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.sink ListSink

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.sink OutputSink

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.source CsvSource

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.matching DatasetMatchingTask

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.executor SeriesExecutor

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.tree TreeExplorer

.. java:import:: es.thinkingmachin.linksight.imatch.server Server

.. java:import:: java.io IOException

Main
====

.. java:package:: es.thinkingmachin.linksight.imatch.main
   :noindex:

.. java:type:: public class Main

Methods
-------
main
^^^^

.. java:method:: public static void main(String[] args) throws Throwable
   :outertype: Main

   The main method. Allows user to choose between different modes: server, test, explorer, and manual.

   :param args: the command line arguments
   :throws Throwable: if mode value is invalid.

