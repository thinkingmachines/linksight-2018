package es.thinkingmachin.linksight.imatch.matcher.tree;

import es.thinkingmachin.linksight.imatch.matcher.core.Interlevel;
import es.thinkingmachin.linksight.imatch.matcher.model.FuzzyStringMap;

import java.util.HashMap;

public class AddressTreeNode {

    // Identifiers
    public final String term;
    public final Interlevel level;

    // Child-related fields
    public final FuzzyStringMap<AddressTreeNode> fuzzyStringMap;
    public final HashMap<String, AddressTreeNode> children = new HashMap<>();   // Standard Term -> AddressTreeNode

    public AddressTreeNode(String term, Interlevel level) {
        this.fuzzyStringMap = new FuzzyStringMap<>();
        this.term = term;
        this.level = level;
    }

    public void addChild(Interlevel level, String stdTerm, String aliasTerm) {
        if (!children.containsKey(stdTerm)) {
            // First time to add child node
            AddressTreeNode newNode = new AddressTreeNode(stdTerm, level);
            children.put(stdTerm, newNode);
            fuzzyStringMap.put(stdTerm, newNode);
        }
        // Add alias term
        fuzzyStringMap.addKeyAlias(stdTerm, aliasTerm);
    }

    public AddressTreeNode getChild(String stdTerm) {
        return children.get(stdTerm);
    }
}
