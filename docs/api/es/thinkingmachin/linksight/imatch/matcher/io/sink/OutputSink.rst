.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.reference ReferenceMatch

.. java:import:: java.io IOException

OutputSink
==========

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.io.sink
   :noindex:

.. java:type:: public interface OutputSink

Methods
-------
addMatch
^^^^^^^^

.. java:method::  void addMatch(long index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException
   :outertype: OutputSink

close
^^^^^

.. java:method::  boolean close()
   :outertype: OutputSink

getName
^^^^^^^

.. java:method::  String getName()
   :outertype: OutputSink

getSize
^^^^^^^

.. java:method::  int getSize()
   :outertype: OutputSink

open
^^^^

.. java:method::  void open() throws IOException
   :outertype: OutputSink

