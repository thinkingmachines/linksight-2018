.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.reference ReferenceMatch

.. java:import:: java.io IOException

.. java:import:: java.util LinkedList

.. java:import:: java.util List

ListSink
========

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.io.sink
   :noindex:

.. java:type:: public class ListSink implements OutputSink

Methods
-------
addMatch
^^^^^^^^

.. java:method:: @Override public void addMatch(long index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException
   :outertype: ListSink

close
^^^^^

.. java:method:: @Override public boolean close()
   :outertype: ListSink

getMatches
^^^^^^^^^^

.. java:method:: public List<ReferenceMatch> getMatches()
   :outertype: ListSink

getName
^^^^^^^

.. java:method:: @Override public String getName()
   :outertype: ListSink

getSize
^^^^^^^

.. java:method:: @Override public int getSize()
   :outertype: ListSink

open
^^^^

.. java:method:: @Override public void open() throws IOException
   :outertype: ListSink

