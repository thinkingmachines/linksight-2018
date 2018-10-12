package es.thinkingmachin.linksight.imatch.matcher.tree;

import es.thinkingmachin.linksight.imatch.matcher.model.FuzzyStringMap;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.util.*;

public class AddressTreeNode {

    // Node Properties
    private String origTerm;
    public final String psgc;
    private ArrayList<String> aliases;

    // Child-related
    public final FuzzyStringMap<AddressTreeNode> fuzzyStringMap;
    public final List<AddressTreeNode> children = new ArrayList<>();  // Can be updated at child-add time
    private final HashMap<String, AddressTreeNode> childrenMap = new HashMap<>();  // Maps origTerm -> node. Can only be created at indexing time

    // Parent-related
    public final AddressTreeNode parent;

    AddressTreeNode(String psgc, AddressTreeNode parent) {
        this.fuzzyStringMap = new FuzzyStringMap<>();
        this.aliases = new ArrayList<>();
        this.psgc = psgc;
        this.parent = parent;
    }

    static AddressTreeNode createRoot() {
        return new AddressTreeNode(null, null);
    }

    void addChild(AddressTreeNode node) {
        children.add(node);
    }

    String getOrigTerm() {
        return origTerm;
    }

    void createSearchIndex() {
        for (AddressTreeNode child : children) {
            assert child.origTerm != null;
            childrenMap.put(child.origTerm, child);
            fuzzyStringMap.put(child.origTerm, child);
            for (String alias : child.aliases) {
                fuzzyStringMap.addKeyAlias(child.origTerm, alias);
            }
        }
    }

    void addAlias(String alias, boolean isOriginal) {
        if (isOriginal) {
            if (origTerm != null) {
                System.out.println("Warning: more than one original term for "+origTerm);
            }
            origTerm = alias;
        }
        aliases.add(alias);
    }

    Set<String> getChildTerms() {
        return childrenMap.keySet();
    }

    AddressTreeNode getChildWithOrigTerm(String origTerm) {
        return childrenMap.getOrDefault(origTerm, null);
    }

    public List<AddressTreeNode> getAncestry() {
        AddressTreeNode node = this;
        LinkedList<AddressTreeNode> ancestry = new LinkedList<>();
        while (node != null) {
            ancestry.addFirst(node);
            node = node.parent;
        }
        return ancestry;
    }
}
