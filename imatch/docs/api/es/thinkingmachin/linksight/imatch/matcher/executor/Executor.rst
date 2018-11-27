.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.io.source InputSource

.. java:import:: java.util.function Consumer

Executor
========

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.executor
   :noindex:

.. java:type:: public interface Executor

   This class serves as the interface for all executor instances for matching addresses.

Methods
-------
execute
^^^^^^^

.. java:method::  void execute(InputSource source, Consumer<Address> task)
   :outertype: Executor

