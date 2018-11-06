.. java:import:: de.siegmar.fastcsv.reader CsvParser

.. java:import:: de.siegmar.fastcsv.reader CsvReader

.. java:import:: java.io File

.. java:import:: java.io IOException

.. java:import:: java.nio.charset StandardCharsets

Dataset
=======

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.dataset
   :noindex:

.. java:type:: public class Dataset

   This class encapsulates the information about the dataset file uploaded by the user. It includes the path to where the CSV file is located and the fields (barangay, municity, province) specified by the user that are included in the dataset.

Fields
------
csvPath
^^^^^^^

.. java:field:: public final String csvPath
   :outertype: Dataset

locFields
^^^^^^^^^

.. java:field:: public final String[] locFields
   :outertype: Dataset

Constructors
------------
Dataset
^^^^^^^

.. java:constructor:: public Dataset(String csvPath, String[] locFields)
   :outertype: Dataset

Methods
-------
getCsvParser
^^^^^^^^^^^^

.. java:method:: public CsvParser getCsvParser() throws IOException
   :outertype: Dataset

   Instantiates a CSV reader and returns a CSV parser.

   :throws IOException:
   :return: a new CSV parser

