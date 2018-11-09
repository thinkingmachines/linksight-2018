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

   This class encapsulates information about the list of matched values. It adds the matched values to a list.

Methods
-------
addMatch
^^^^^^^^

.. java:method:: @Override public void addMatch(long index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException
   :outertype: ListSink

   Adds the match to the list.

   :param index:
   :param srcAddress:
   :param matchTime:
   :param match:
   :throws IOException: if file is invalid

close
^^^^^

.. java:method:: @Override public boolean close()
   :outertype: ListSink

getMatches
^^^^^^^^^^

.. java:method:: public List<ReferenceMatch> getMatches()
   :outertype: ListSink

   :return: the list of matched locations

getName
^^^^^^^

.. java:method:: @Override public String getName()
   :outertype: ListSink

   :return: a string stating the number of matches in the list

getSize
^^^^^^^

.. java:method:: @Override public int getSize()
   :outertype: ListSink

   :return: the total number of matches in the list

open
^^^^

.. java:method:: @Override public void open() throws IOException
   :outertype: ListSink

   Initialize the list of matches.

   :throws IOException: if file is invalid

