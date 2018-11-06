.. java:import:: de.siegmar.fastcsv.writer CsvAppender

.. java:import:: de.siegmar.fastcsv.writer CsvWriter

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.reference ReferenceMatch

.. java:import:: java.io File

.. java:import:: java.io IOException

.. java:import:: java.nio.charset StandardCharsets

.. java:import:: java.nio.file Files

.. java:import:: java.nio.file Path

.. java:import:: java.nio.file Paths

LinkSightCsvSink
================

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.io.sink
   :noindex:

.. java:type:: public class LinkSightCsvSink implements OutputSink

Methods
-------
addMatch
^^^^^^^^

.. java:method:: @Override public void addMatch(long index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException
   :outertype: LinkSightCsvSink

close
^^^^^

.. java:method:: @Override public boolean close()
   :outertype: LinkSightCsvSink

getName
^^^^^^^

.. java:method:: @Override public String getName()
   :outertype: LinkSightCsvSink

getOutputFile
^^^^^^^^^^^^^

.. java:method:: public File getOutputFile()
   :outertype: LinkSightCsvSink

getSize
^^^^^^^

.. java:method:: @Override public int getSize()
   :outertype: LinkSightCsvSink

open
^^^^

.. java:method:: @Override public void open() throws IOException
   :outertype: LinkSightCsvSink

