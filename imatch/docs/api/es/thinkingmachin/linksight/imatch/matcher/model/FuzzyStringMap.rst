.. java:import:: com.google.common.collect HashMultimap

.. java:import:: de.cxp.predict PreDict

.. java:import:: de.cxp.predict.api PreDictSettings

.. java:import:: de.cxp.predict.api SuggestItem

.. java:import:: de.cxp.predict.customizing CommunityCustomization

.. java:import:: de.cxp.predict.customizing PreDictCustomizing

.. java:import:: org.apache.commons.math3.util Pair

.. java:import:: java.util.regex Pattern

.. java:import:: java.util.stream Collectors

FuzzyStringMap
==============

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.model
   :noindex:

.. java:type:: public class FuzzyStringMap<T>

   This class encapsulates information about the PreDict model. It consists of the PreDict model, the multi map of nodes and its values, and the customization settings for the PreDict model.

   :param <T>:

Fields
------
customization
^^^^^^^^^^^^^

.. java:field:: public PreDictCustomizing customization
   :outertype: FuzzyStringMap

preDict
^^^^^^^

.. java:field:: public final PreDict preDict
   :outertype: FuzzyStringMap

Constructors
------------
FuzzyStringMap
^^^^^^^^^^^^^^

.. java:constructor:: public FuzzyStringMap()
   :outertype: FuzzyStringMap

Methods
-------
getExact
^^^^^^^^

.. java:method:: public Set<T> getExact(String key)
   :outertype: FuzzyStringMap

getFuzzy
^^^^^^^^

.. java:method:: public Set<Pair<T, Double>> getFuzzy(String key)
   :outertype: FuzzyStringMap

   Searches the key using the predict model and returns a list of suggestions. Each key of the suggested items is looked up in the multi map, getting its values. Each value, together with the computed proximity in PreDict is added to a list called fuzzyPairs.

   :param key: the subphrase to be searched using the PreDict model
   :return: a set of values of the suggested items during the search and their corresponding proximity

put
^^^

.. java:method:: public void put(String key, T value)
   :outertype: FuzzyStringMap

   Creates a key using the specified PreDict customization settings and adds the key-value pair to the multimap.

   :param key:
   :param value:

