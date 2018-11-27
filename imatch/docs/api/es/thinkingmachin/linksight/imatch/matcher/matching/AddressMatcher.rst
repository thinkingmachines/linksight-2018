.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.reference ReferenceMatch

.. java:import:: java.util List

AddressMatcher
==============

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.matching
   :noindex:

.. java:type:: public interface AddressMatcher

   This class serves as the interface for getting the top matches for matching algorithms.

Methods
-------
getTopMatches
^^^^^^^^^^^^^

.. java:method::  List<ReferenceMatch> getTopMatches(Address address, int numMatches)
   :outertype: AddressMatcher

