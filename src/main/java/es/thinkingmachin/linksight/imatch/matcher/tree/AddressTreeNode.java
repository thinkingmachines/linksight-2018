package es.thinkingmachin.linksight.imatch.matcher.tree;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Objects;

public class AddressTreeNode {

    // Node Properties
    private String origTerm;
    public final String psgc;
    ArrayList<String> aliases;

    // Child-related
    public AddressTreeNodeIndex childIndex;
    public final List<AddressTreeNode> children = new ArrayList<>();

    // Parent-related
    public final AddressTreeNode parent;

    AddressTreeNode(String psgc, AddressTreeNode parent) {
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
        childIndex = new AddressTreeNodeIndex();
        children.forEach(child -> childIndex.indexChild(child));
    }

    void addAlias(String alias, boolean isOriginal) {
        if (isOriginal) {
            if (origTerm != null) {
                // One known instance: NCR, CITY OF MANILA, FIRST DISTRICT (NOT A PROVINCE)
                System.out.println("Warning: more than one original term for "+origTerm);
            }
            origTerm = alias;
        }
        aliases.add(alias);
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

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AddressTreeNode that = (AddressTreeNode) o;
        return Objects.equals(origTerm, that.origTerm) &&
                Objects.equals(psgc, that.psgc);
    }

    @Override
    public int hashCode() {
        return Objects.hash(origTerm, psgc);
    }
}
