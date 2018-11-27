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

   This class encapsulates information about the CSV output file. It facilitates appending and writing the original data, the matched values, and the other statistics on a new csv file.

Methods
-------
addMatch
^^^^^^^^

.. java:method:: @Override public void addMatch(long index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException
   :outertype: LinkSightCsvSink

   Writes the original location with its matched fields, together with the psgc, total score, match time, and match type

   :param index: row number of the address
   :param srcAddress: the source address in the input dataset
   :param matchTime: the total matching time
   :param match: the matched values
   :throws IOException: if output file is invalid

close
^^^^^

.. java:method:: @Override public boolean close()
   :outertype: LinkSightCsvSink

   Closes the CSV writer

   :return: true if successful, false otherwise

getName
^^^^^^^

.. java:method:: @Override public String getName()
   :outertype: LinkSightCsvSink

   :return: the path of the output file

getOutputFile
^^^^^^^^^^^^^

.. java:method:: public File getOutputFile()
   :outertype: LinkSightCsvSink

   :return: the output file with the matched locations and psgc

getSize
^^^^^^^

.. java:method:: @Override public int getSize()
   :outertype: LinkSightCsvSink

   :return: the number of rows in the output file

open
^^^^

.. java:method:: @Override public void open() throws IOException
   :outertype: LinkSightCsvSink

   Opens and starts the CSV writer

   :throws IOException: if file is invalid

