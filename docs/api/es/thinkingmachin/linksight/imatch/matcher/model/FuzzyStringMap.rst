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

put
^^^

.. java:method:: public void put(String key, T value)
   :outertype: FuzzyStringMap

