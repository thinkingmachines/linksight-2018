.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.source InputSource

.. java:import:: java.util List

.. java:import:: java.util.concurrent ExecutionException

.. java:import:: java.util.concurrent ForkJoinPool

.. java:import:: java.util.function Consumer

.. java:import:: java.util.stream Collectors

ParallelExecutor
================

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.executor
   :noindex:

.. java:type:: public class ParallelExecutor implements Executor

   This class serves as the task executor for parallel processing.

Methods
-------
execute
^^^^^^^

.. java:method:: @Override public void execute(InputSource source, Consumer<Address> task)
   :outertype: ParallelExecutor

   Executes threads in parallel.

   :param source: the source data
   :param task: the process to be run

