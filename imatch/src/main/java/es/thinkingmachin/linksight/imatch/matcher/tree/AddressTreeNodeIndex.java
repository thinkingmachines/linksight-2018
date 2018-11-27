package es.thinkingmachin.linksight.imatch.matcher.tree;

import es.thinkingmachin.linksight.imatch.matcher.model.FuzzyStringMap;

import java.util.HashMap;

/**
 * This class encapsulates the information about the index of each node.
 * It includes the original terms and aliases for the children of its corresponding node.
 * The AddressTreeNodeIndex is used in the fuzzy matching algorithm.
 */
public class AddressTreeNodeIndex {
    public final FuzzyStringMap<AddressTreeNode> namesFuzzyMap;
    public final HashMap<String, AddressTreeNode> origTermMap;


    public AddressTreeNodeIndex() {
        namesFuzzyMap = new FuzzyStringMap<>();
        origTermMap = new HashMap<>();
    }

    /**
     * Maps the original term and the aliases of the child to the child node
     * @param child the child node of the current node
     */
    public void indexChild(AddressTreeNode child) {
        String origTerm = child.getOrigTerm();
        assert origTerm != null;
        origTermMap.put(origTerm, child);
        for (String alias : child.aliases) {
            namesFuzzyMap.put(alias, child);
        }
    }

    /**
     * @param origTerm the original name for the location
     * @return the node mapped to the origTerm, or null if the origTerm is not mapped
     */
    AddressTreeNode getNodeWithOrigTerm(String origTerm) {
        return origTermMap.getOrDefault(origTerm, null);
    }
}
