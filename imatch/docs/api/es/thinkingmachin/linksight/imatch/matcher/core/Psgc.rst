Psgc
====

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.core
   :noindex:

.. java:type:: public class Psgc

   This class serves as a utility class for the psgc field. It allows the program to get the parent psgc and the level where the psgc is located.

Fields
------
NONE
^^^^

.. java:field:: public static final long NONE
   :outertype: Psgc

Methods
-------
getLevel
^^^^^^^^

.. java:method:: public static int getLevel(long psgc)
   :outertype: Psgc

   Computes for the level the current psgc is in.

   :param psgc: the psgc being processed
   :return: the level where the psgc belongs

getLevel
^^^^^^^^

.. java:method:: public static int getLevel(String psgc)
   :outertype: Psgc

   Computes for the level the current psgc is in.

   :param psgc: the psgc being processed in string format
   :return: the level where the psgc belongs

getParent
^^^^^^^^^

.. java:method:: public static long getParent(long psgc)
   :outertype: Psgc

   Computes for the parent psgc of the given psgc.

   :param psgc: the psgc being processed
   :return: the parent psgc

