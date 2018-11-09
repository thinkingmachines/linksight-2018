.. java:import:: es.thinkingmachin.linksight.imatch.matcher.tree AddressTreeNode

.. java:import:: java.util Arrays

.. java:import:: java.util Comparator

.. java:import:: java.util List

BfsTraversed
============

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.tree.matcher
   :noindex:

.. java:type:: public class BfsTraversed

   This class encapsulates information on each entry in the BFS queue. It includes information about the node, the array of scores, its overall score and the remaining terms in the search strings to be compared.

Fields
------
node
^^^^

.. java:field:: final AddressTreeNode node
   :outertype: BfsTraversed

overallScore
^^^^^^^^^^^^

.. java:field:: final double overallScore
   :outertype: BfsTraversed

remainingTerms
^^^^^^^^^^^^^^

.. java:field:: final List<String>[] remainingTerms
   :outertype: BfsTraversed

scores
^^^^^^

.. java:field:: final double[] scores
   :outertype: BfsTraversed

Constructors
------------
BfsTraversed
^^^^^^^^^^^^

.. java:constructor::  BfsTraversed(AddressTreeNode node, double score, BfsTraversed parent, List<String>[] remainingTerms)
   :outertype: BfsTraversed

Methods
-------
createComparator
^^^^^^^^^^^^^^^^

.. java:method:: public static Comparator<BfsTraversed> createComparator()
   :outertype: BfsTraversed

getTotalRemaining
^^^^^^^^^^^^^^^^^

.. java:method:: public int getTotalRemaining()
   :outertype: BfsTraversed

   Get the total number of remaining search strings

   :return: the number of remaining search strings

getWordCoverageScore
^^^^^^^^^^^^^^^^^^^^

.. java:method:: static double getWordCoverageScore(int remainingWords)
   :outertype: BfsTraversed

   Computes for the score of the remaining words in the search substrings

   :param remainingWords: the number of remaining words in the search strings
   :return: the word coverage score

