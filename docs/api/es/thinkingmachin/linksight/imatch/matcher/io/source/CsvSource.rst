.. java:import:: de.siegmar.fastcsv.reader CsvParser

.. java:import:: de.siegmar.fastcsv.reader CsvRow

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset Dataset

.. java:import:: java.io IOException

.. java:import:: java.util NoSuchElementException

CsvSource
=========

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.io.source
   :noindex:

.. java:type:: public class CsvSource implements InputSource

   This class encapsulates information about the CSV input data. It contains the CSV parser which allows the user to loop through each row.

Constructors
------------
CsvSource
^^^^^^^^^

.. java:constructor:: public CsvSource(Dataset dataset)
   :outertype: CsvSource

Methods
-------
close
^^^^^

.. java:method:: @Override public boolean close()
   :outertype: CsvSource

   Closes the CSV parser

   :return: true if closing is successful

getCurrentCount
^^^^^^^^^^^^^^^

.. java:method:: public int getCurrentCount()
   :outertype: CsvSource

   :return: the current count of rows passed

getName
^^^^^^^

.. java:method:: @Override public String getName()
   :outertype: CsvSource

   :return: the filename of the CSV dataset

hasNext
^^^^^^^

.. java:method:: @Override public boolean hasNext()
   :outertype: CsvSource

   :return: true if the next row is not null

next
^^^^

.. java:method:: @Override public Address next()
   :outertype: CsvSource

   Gets the next row and instantiates a new Address object

   :return: the created address object from the given row

open
^^^^

.. java:method:: @Override public void open() throws IOException
   :outertype: CsvSource

   Opens and starts the CSV parser

   :throws IOException: if file is invalid

