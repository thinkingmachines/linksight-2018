.. java:import:: es.thinkingmachin.linksight.imatch.matcher.model FuzzyStringMap

.. java:import:: java.util HashMap

AddressTreeNodeIndex
====================

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.tree
   :noindex:

.. java:type:: public class AddressTreeNodeIndex

   This class encapsulates the information about the index of each node. It includes the original terms and aliases for the children of its corresponding node. The AddressTreeNodeIndex is used in the fuzzy matching algorithm.

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

   :param origTerm: the original name for the location
   :return: the node mapped to the origTerm, or null if the origTerm is not mapped

indexChild
^^^^^^^^^^

.. java:method:: public void indexChild(AddressTreeNode child)
   :outertype: AddressTreeNodeIndex

   Maps the original term and the aliases of the child to the child node

   :param child: the child node of the current node

