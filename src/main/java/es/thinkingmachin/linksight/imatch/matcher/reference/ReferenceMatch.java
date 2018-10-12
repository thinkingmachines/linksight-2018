package es.thinkingmachin.linksight.imatch.matcher.reference;

import es.thinkingmachin.linksight.imatch.matcher.tree.AddressTreeNode;

public class ReferenceMatch {
    public final AddressTreeNode match;
    public final double score;

    public ReferenceMatch(AddressTreeNode match, double score) {
        this.match = match;
        this.score = score;
    }

    @Override
    public String toString() {
        return match.toString() + " score: " + score;
    }
}
