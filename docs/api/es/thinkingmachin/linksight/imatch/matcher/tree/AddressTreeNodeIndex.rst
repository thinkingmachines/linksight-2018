.. java:import:: es.thinkingmachin.linksight.imatch.matcher.model FuzzyStringMap

.. java:import:: java.util HashMap

AddressTreeNodeIndex
====================

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.tree
   :noindex:

.. java:type:: public class AddressTreeNodeIndex

Fields
------
namesFuzzyMap
^^^^^^^^^^^^^

.. java:field:: public final FuzzyStringMap<AddressTreeNode> namesFuzzyMap
   :outertype: AddressTreeNodeIndex

origTermMap
^^^^^^^^^^^

.. java:field:: public final HashMap<String, AddressTreeNode> origTermMap
   :outertype: AddressTreeNodeIndex

Constructors
------------
AddressTreeNodeIndex
^^^^^^^^^^^^^^^^^^^^

.. java:constructor:: public AddressTreeNodeIndex()
   :outertype: AddressTreeNodeIndex

Methods
-------
getNodeWithOrigTerm
^^^^^^^^^^^^^^^^^^^

.. java:method::  AddressTreeNode getNodeWithOrigTerm(String origTerm)
   :outertype: AddressTreeNodeIndex

indexChild
^^^^^^^^^^

.. java:method:: public void indexChild(AddressTreeNode child)
   :outertype: AddressTreeNodeIndex

