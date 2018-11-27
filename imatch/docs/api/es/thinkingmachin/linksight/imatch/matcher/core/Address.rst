.. java:import:: de.siegmar.fastcsv.reader CsvRow

.. java:import:: sun.reflect.generics.reflectiveObjects NotImplementedException

.. java:import:: java.util Arrays

Address
=======

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.core
   :noindex:

.. java:type:: public class Address

   This class stores the array of location terms in an object, together with its corresponding row number.

Fields
------
rowNum
^^^^^^

.. java:field:: public final long rowNum
   :outertype: Address

terms
^^^^^

.. java:field:: public final String[] terms
   :outertype: Address

Constructors
------------
Address
^^^^^^^

.. java:constructor:: public Address(String[] terms, long rowNum)
   :outertype: Address

Methods
-------
equals
^^^^^^

.. java:method:: @Override public boolean equals(Object o)
   :outertype: Address

   Checks if two address objects are equal by comparing its terms.

   :param o: the object being compared
   :return: true if the two objects are equal, false otherwise

fromCsvRow
^^^^^^^^^^

.. java:method:: public static Address fromCsvRow(CsvRow csvRow, String[] locFields)
   :outertype: Address

   Parses the CSV row to convert to an Address object.

   :param csvRow: the CSV row being processed
   :param locFields: the location fields (barangay, municity, province)
   :return: a new instance of an Address object

hashCode
^^^^^^^^

.. java:method:: @Override public int hashCode()
   :outertype: Address

   :return: a hashcode value for the object using the hashcode of the array of terms

toString
^^^^^^^^

.. java:method:: @Override public String toString()
   :outertype: Address

   :return: a string representation of the array of terms

