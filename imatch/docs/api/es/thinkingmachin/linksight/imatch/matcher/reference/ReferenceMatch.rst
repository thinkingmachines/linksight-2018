.. java:import:: es.thinkingmachin.linksight.imatch.matcher.tree AddressTreeNode

.. java:import:: java.util Arrays

ReferenceMatch
==============

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.reference
   :noindex:

.. java:type:: public class ReferenceMatch

   This class encapsulates the information about the matched value. It includes information about the score for the match and the list of scores for each interlevel.

Fields
------
match
^^^^^

.. java:field:: public final AddressTreeNode match
   :outertype: ReferenceMatch

score
^^^^^

.. java:field:: public final double score
   :outertype: ReferenceMatch

scores
^^^^^^

.. java:field:: public final double[] scores
   :outertype: ReferenceMatch

Constructors
------------
ReferenceMatch
^^^^^^^^^^^^^^

.. java:constructor:: public ReferenceMatch(AddressTreeNode match, double score, double[] scores)
   :outertype: ReferenceMatch

Methods
-------
toString
^^^^^^^^

.. java:method:: @Override public String toString()
   :outertype: ReferenceMatch

   Converts to string the final score and the list of scores for each interlevel

   :return: string of the final score and the list of scores for each interlevel

