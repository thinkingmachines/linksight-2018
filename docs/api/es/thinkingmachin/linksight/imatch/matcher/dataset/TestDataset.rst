TestDataset
===========

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.dataset
   :noindex:

.. java:type:: public class TestDataset extends Dataset

   This class encapsulates the information about the test datasets.

Fields
------
correctPsgcField
^^^^^^^^^^^^^^^^

.. java:field:: public final String correctPsgcField
   :outertype: TestDataset

name
^^^^

.. java:field:: public final String name
   :outertype: TestDataset

Constructors
------------
TestDataset
^^^^^^^^^^^

.. java:constructor:: public TestDataset(String name, String csvPath, String[] dirtyLocFields, String correctPsgcField)
   :outertype: TestDataset

Methods
-------
hasCorrectField
^^^^^^^^^^^^^^^

.. java:method:: public boolean hasCorrectField()
   :outertype: TestDataset

   Checks if the test dataset has a correct psgc column

   :return: true if a correct psgc column exists, false otherwise.

