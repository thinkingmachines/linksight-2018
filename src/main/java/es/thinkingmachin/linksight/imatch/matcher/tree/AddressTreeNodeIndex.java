package es.thinkingmachin.linksight.imatch.matcher.tree;

import es.thinkingmachin.linksight.imatch.matcher.model.FuzzyStringMap;

import java.util.HashMap;
import java.util.Set;

public class AddressTreeNodeIndex {
    final FuzzyStringMap<AddressTreeNode> namesFuzzyMap;
    final HashMap<String, AddressTreeNode> origTermMap;


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

    Set<String> getOrigTerms() {
        return origTermMap.keySet();
    }

    AddressTreeNode getNodeWithOrigTerm(String origTerm) {
        return origTermMap.getOrDefault(origTerm, null);
    }
}
