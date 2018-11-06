.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Util

.. java:import:: java.util ArrayList

.. java:import:: java.util LinkedList

.. java:import:: java.util List

.. java:import:: java.util Objects

.. java:import:: java.util.stream Collectors

AddressTreeNode
===============

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.tree
   :noindex:

.. java:type:: public class AddressTreeNode

Fields
------
address
^^^^^^^

.. java:field:: public String[] address
   :outertype: AddressTreeNode

aliases
^^^^^^^

.. java:field::  ArrayList<String> aliases
   :outertype: AddressTreeNode

childIndex
^^^^^^^^^^

.. java:field:: public AddressTreeNodeIndex childIndex
   :outertype: AddressTreeNode

children
^^^^^^^^

.. java:field:: public final List<AddressTreeNode> children
   :outertype: AddressTreeNode

maxChildAliasWords
^^^^^^^^^^^^^^^^^^

.. java:field:: public int maxChildAliasWords
   :outertype: AddressTreeNode

parent
^^^^^^

.. java:field:: public final AddressTreeNode parent
   :outertype: AddressTreeNode

psgc
^^^^

.. java:field:: public final String psgc
   :outertype: AddressTreeNode

Constructors
------------
AddressTreeNode
^^^^^^^^^^^^^^^

.. java:constructor::  AddressTreeNode(String psgc, AddressTreeNode parent)
   :outertype: AddressTreeNode

Methods
-------
addAlias
^^^^^^^^

.. java:method::  void addAlias(String alias, boolean isOriginal)
   :outertype: AddressTreeNode

addChild
^^^^^^^^

.. java:method::  void addChild(AddressTreeNode node)
   :outertype: AddressTreeNode

createRoot
^^^^^^^^^^

.. java:method:: static AddressTreeNode createRoot()
   :outertype: AddressTreeNode

createSearchIndex
^^^^^^^^^^^^^^^^^

.. java:method::  void createSearchIndex()
   :outertype: AddressTreeNode

equals
^^^^^^

.. java:method:: @Override public boolean equals(Object o)
   :outertype: AddressTreeNode

getAncestry
^^^^^^^^^^^

.. java:method:: public List<AddressTreeNode> getAncestry()
   :outertype: AddressTreeNode

getOrigTerm
^^^^^^^^^^^

.. java:method::  String getOrigTerm()
   :outertype: AddressTreeNode

hasChildren
^^^^^^^^^^^

.. java:method:: public boolean hasChildren()
   :outertype: AddressTreeNode

hashCode
^^^^^^^^

.. java:method:: @Override public int hashCode()
   :outertype: AddressTreeNode

toString
^^^^^^^^

.. java:method:: @Override public String toString()
   :outertype: AddressTreeNode

