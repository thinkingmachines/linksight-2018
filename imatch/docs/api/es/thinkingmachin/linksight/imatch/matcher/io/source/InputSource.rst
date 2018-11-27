.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: java.io IOException

.. java:import:: java.util Iterator

.. java:import:: java.util Spliterator

.. java:import:: java.util Spliterators

.. java:import:: java.util.stream Stream

.. java:import:: java.util.stream StreamSupport

InputSource
===========

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.io.source
   :noindex:

.. java:type:: public interface InputSource extends Iterator<Address>

   This class serves as the interface for all input files and sources.

Methods
-------
close
^^^^^

.. java:method::  boolean close()
   :outertype: InputSource

getCurrentCount
^^^^^^^^^^^^^^^

.. java:method::  int getCurrentCount()
   :outertype: InputSource

getName
^^^^^^^

.. java:method::  String getName()
   :outertype: InputSource

open
^^^^

.. java:method::  void open() throws IOException
   :outertype: InputSource

stream
^^^^^^

.. java:method::  Stream<Address> stream()
   :outertype: InputSource

