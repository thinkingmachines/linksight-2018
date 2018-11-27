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

   This class encapsulates the information about each node in the address tree. It includes information on the psgc, the original term for the location, its aliases, its parent node, and children nodes.

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

   Adds an alias to the list of aliases

   :param alias: the alias of the location
   :param isOriginal: true if it is the original term, false otherwise

addChild
^^^^^^^^

.. java:method::  void addChild(AddressTreeNode node)
   :outertype: AddressTreeNode

   Adds a child to the current node

   :param node: the child node

createRoot
^^^^^^^^^^

.. java:method:: static AddressTreeNode createRoot()
   :outertype: AddressTreeNode

   Creates the root node of the reference tree

   :return: the root node of the tree

createSearchIndex
^^^^^^^^^^^^^^^^^

.. java:method::  void createSearchIndex()
   :outertype: AddressTreeNode

   Creates a search index for the current node. The search index contains the aliases of all its children nodes. This method also initializes the address of the node.

equals
^^^^^^

.. java:method:: @Override public boolean equals(Object o)
   :outertype: AddressTreeNode

   Checks if two nodes are equal. Equality is defined as having the same original name and the same psg code.

   :param o: the node being compared
   :return: true if they are equal, false otherwise

getAncestry
^^^^^^^^^^^

.. java:method:: public List<AddressTreeNode> getAncestry()
   :outertype: AddressTreeNode

   :return: the parent nodes of the node up to the root

getOrigTerm
^^^^^^^^^^^

.. java:method::  String getOrigTerm()
   :outertype: AddressTreeNode

   :return: the original name for the location

hasChildren
^^^^^^^^^^^

.. java:method:: public boolean hasChildren()
   :outertype: AddressTreeNode

   Checks if the node has children

   :return: true if the node has children, false otherwise

hashCode
^^^^^^^^

.. java:method:: @Override public int hashCode()
   :outertype: AddressTreeNode

toString
^^^^^^^^

.. java:method:: @Override public String toString()
   :outertype: AddressTreeNode

   Converts to string the address (province, municity, barangay) of the node

   :return: the string representation of the node

