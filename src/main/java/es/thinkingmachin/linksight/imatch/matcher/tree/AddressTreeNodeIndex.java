package es.thinkingmachin.linksight.imatch.matcher.tree;

import es.thinkingmachin.linksight.imatch.matcher.model.FuzzyStringMap;

import java.util.HashMap;

public class AddressTreeNodeIndex {
    public final FuzzyStringMap<AddressTreeNode> namesFuzzyMap;
    public final HashMap<String, AddressTreeNode> origTermMap;


    public AddressTreeNodeIndex() {
        namesFuzzyMap = new FuzzyStringMap<>();
        origTermMap = new HashMap<>();
    }

    public void indexChild(AddressTreeNode child) {
        String origTerm = child.getOrigTerm();
        assert origTerm != null;
        origTermMap.put(origTerm, child);
        for (String alias : child.aliases) {
            namesFuzzyMap.put(alias, child);
        }
    }

    AddressTreeNode getNodeWithOrigTerm(String origTerm) {
        return origTermMap.getOrDefault(origTerm, null);
    }
}
