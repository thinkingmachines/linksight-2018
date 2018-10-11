package es.thinkingmachin.linksight.imatch.matcher.tree;

import es.thinkingmachin.linksight.imatch.matcher.core.Interlevel;
import es.thinkingmachin.linksight.imatch.matcher.model.FuzzyStringMap;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceRow;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

public class AddressTreeNode {

    // Identifiers
    public final String term;
    public final Interlevel level;

    // Child-related
    public final FuzzyStringMap<AddressTreeNode> fuzzyStringMap;
    public final HashMap<String, AddressTreeNode> children = new HashMap<>();   // Standard Term -> AddressTreeNode

    // Parent-related
    public final AddressTreeNode parent;

    private ReferenceRow referenceRow;
    private static int psgcBad = 0;

    public AddressTreeNode(String term, Interlevel level, AddressTreeNode parent) {
        this.fuzzyStringMap = new FuzzyStringMap<>();
        this.term = term;
        this.level = level;
        this.parent = parent;
    }

    public void addChild(Interlevel level, String stdTerm, String aliasTerm) {
        if (!children.containsKey(stdTerm)) {
            // First time to add child node
            AddressTreeNode newNode = new AddressTreeNode(stdTerm, level, this);
            children.put(stdTerm, newNode);
            fuzzyStringMap.put(stdTerm, newNode);
        }
        // Add alias term
        fuzzyStringMap.addKeyAlias(stdTerm, aliasTerm);
    }

    public AddressTreeNode getChild(String stdTerm) {
        return children.get(stdTerm);
    }

    public ReferenceRow getReferenceRow() {
        return referenceRow;
    }

    public void setReferenceRow(ReferenceRow referenceRow) {
        if (this.referenceRow != null && referenceRow.psgc != this.referenceRow.psgc) {
//            throw new Error("Reference row has already been set: from "+this.referenceRow.psgc+" to "+referenceRow.psgc);
            psgcBad++;
            System.out.println("PSGC BAD: "+psgcBad);
        }
        this.referenceRow = referenceRow;
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
