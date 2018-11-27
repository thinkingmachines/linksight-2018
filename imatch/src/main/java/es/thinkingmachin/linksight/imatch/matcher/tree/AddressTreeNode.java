package es.thinkingmachin.linksight.imatch.matcher.tree;

import es.thinkingmachin.linksight.imatch.matcher.core.Util;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

/**
 * This class encapsulates the information about each node in the address tree.
 * It includes information on the psgc, the original term for the location,
 * its aliases, its parent node, and children nodes.
 */
public class AddressTreeNode {

    // Node Properties
    private String origTerm;
    public final String psgc;
    ArrayList<String> aliases;

    // Child-related
    public AddressTreeNodeIndex childIndex;
    public int maxChildAliasWords;
    public final List<AddressTreeNode> children = new ArrayList<>();

    // Parent-related
    public final AddressTreeNode parent;
    public String[] address; // order: province, municity, bgy

    AddressTreeNode(String psgc, AddressTreeNode parent) {
        this.aliases = new ArrayList<>();
        this.psgc = psgc;
        this.parent = parent;
    }

    /**
     * Creates the root node of the reference tree
     * @return the root node of the tree
     */
    static AddressTreeNode createRoot() {
        return new AddressTreeNode(null, null);
    }

    /**
     * @return the original name for the location
     */
    String getOrigTerm() {
        return origTerm;
    }

    /**
     * Adds a child to the current node
     * @param node the child node
     */
    void addChild(AddressTreeNode node) {
        children.add(node);
    }

    /**
     * Creates a search index for the current node.
     * The search index contains the aliases of all its children nodes.
     * This method also initializes the address of the node.
     */
    void createSearchIndex() {
        childIndex = new AddressTreeNodeIndex();
        children.forEach(child -> childIndex.indexChild(child));
        children.forEach(child -> child.aliases.forEach(alias -> {
            maxChildAliasWords = Math.max(Util.splitTerm(alias).length, maxChildAliasWords);
        }));
        address = generateAddress();
    }

    /**
     * Adds an alias to the list of aliases
     * @param alias         the alias of the location
     * @param isOriginal    true if it is the original term, false otherwise
     */
    void addAlias(String alias, boolean isOriginal) {
        if (isOriginal) {
            if (origTerm != null) {
                // One known instance: NCR, CITY OF MANILA, FIRST DISTRICT (NOT A PROVINCE)
                System.out.println("Warning: more than one original term for " + origTerm);
            }
            origTerm = alias;
        }
        aliases.add(alias);
    }

    /**
     * @return the parent nodes of the node up to the root
     */
    public List<AddressTreeNode> getAncestry() {
        AddressTreeNode node = this;
        LinkedList<AddressTreeNode> ancestry = new LinkedList<>();
        while (node != null) {
            ancestry.addFirst(node);
            node = node.parent;
        }
        return ancestry;
    }

    /**
     * Generates the an array for the address of the node
     * in the order of province, municity, and barangay
     * @return an array of location that constitute the address (province, municity, bgy)
     */
    private String[] generateAddress() {
        List<String> strings = getAncestry().stream()
                .map(node -> node.origTerm)
                .collect(Collectors.toList());
        if (strings.size() > 2) {
            strings = strings.subList(2, strings.size());
        }
        return strings.toArray(new String[]{});
    }

    /**
     * Checks if two nodes are equal.
     * Equality is defined as having the same original name
     * and the same psg code.
     * @param o the node being compared
     * @return true if they are equal, false otherwise
     */
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

    /**
     * Checks if the node has children
     * @return true if the node has children, false otherwise
     */
    public boolean hasChildren() {
        return !children.isEmpty();
    }

    /**
     * Converts to string the address (province, municity, barangay) of the node
     * @return the string representation of the node
     */
    @Override
    public String toString() {
        StringBuilder str = new StringBuilder();
        if (address != null) {
            str.append("[");
            str.append(String.join(", ", address));
            str.append("]");
        } else {
            str.append("[Warning: Tree not yet generated]");
        }
        str.append(", PSGC: ");
        str.append(psgc);
        return str.toString();
    }
}
