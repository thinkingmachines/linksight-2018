.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.source InputSource

.. java:import:: java.util.function Consumer

SeriesExecutor
==============

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.executor
   :noindex:

.. java:type:: public class SeriesExecutor implements Executor

   This class serves as the task executor for sequential processing.

Methods
-------
execute
^^^^^^^

.. java:method:: @Override public void execute(InputSource source, Consumer<Address> task)
   :outertype: SeriesExecutor

   Executes threads sequentially.

   :param source: the source data
   :param task: the process to be run

