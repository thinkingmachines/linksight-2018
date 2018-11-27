.. java:import:: de.siegmar.fastcsv.reader CsvParser

.. java:import:: de.siegmar.fastcsv.reader CsvReader

.. java:import:: java.io File

.. java:import:: java.io IOException

.. java:import:: java.nio.charset StandardCharsets

PsgcDataset
===========

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.dataset
   :noindex:

.. java:type:: public class PsgcDataset

   This class encapsulates the information about the psgc dataset. It includes the path to where the CSV file is located, and the headers for the psgc, location, isOriginal, and interlevel columns.

Fields
------
codeField
^^^^^^^^^

.. java:field:: public final String codeField
   :outertype: PsgcDataset

csvPath
^^^^^^^

.. java:field:: public final String csvPath
   :outertype: PsgcDataset

isOrigField
^^^^^^^^^^^

.. java:field:: public final String isOrigField
   :outertype: PsgcDataset

levelField
^^^^^^^^^^

.. java:field:: public final String levelField
   :outertype: PsgcDataset

termField
^^^^^^^^^

.. java:field:: public final String termField
   :outertype: PsgcDataset

Constructors
------------
PsgcDataset
^^^^^^^^^^^

.. java:constructor:: public PsgcDataset(String csvPath, String termField, String isOrigField, String codeField, String levelField)
   :outertype: PsgcDataset

Methods
-------
getCsvParser
^^^^^^^^^^^^

.. java:method:: public CsvParser getCsvParser() throws IOException
   :outertype: PsgcDataset

   Instantiates a CSV reader and returns a CSV parser.

   :throws IOException: if file is invalid
   :return: a new CSV parser

