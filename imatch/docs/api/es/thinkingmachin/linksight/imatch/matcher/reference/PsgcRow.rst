.. java:import:: de.siegmar.fastcsv.reader CsvRow

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset PsgcDataset

PsgcRow
=======

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.reference
   :noindex:

.. java:type:: public class PsgcRow

   This class encapsulates the information about each row in the PSGC dataset. It includes the psgc, location name, its interlevel, its line number in the CSV file, and the row in string format.

Fields
------
csvLineNo
^^^^^^^^^

.. java:field:: public final long csvLineNo
   :outertype: PsgcRow

interlevel
^^^^^^^^^^

.. java:field:: public final String interlevel
   :outertype: PsgcRow

isOriginal
^^^^^^^^^^

.. java:field:: public final boolean isOriginal
   :outertype: PsgcRow

location
^^^^^^^^

.. java:field:: public final String location
   :outertype: PsgcRow

psgc
^^^^

.. java:field:: public final long psgc
   :outertype: PsgcRow

psgcStr
^^^^^^^

.. java:field:: public final String psgcStr
   :outertype: PsgcRow

rowString
^^^^^^^^^

.. java:field:: public final String rowString
   :outertype: PsgcRow

Methods
-------
fromCsvRow
^^^^^^^^^^

.. java:method:: public static PsgcRow fromCsvRow(CsvRow row, PsgcDataset dataset)
   :outertype: PsgcRow

   Creates a new instance of a PSGC row based on the PSGC dataset

   :param row: a row from the psgc dataset
   :param dataset: the psgc dataset object
   :return: an object containing data about each row in the psgc dataset

