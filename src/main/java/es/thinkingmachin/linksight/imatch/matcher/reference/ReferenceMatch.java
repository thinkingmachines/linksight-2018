package es.thinkingmachin.linksight.imatch.matcher.reference;

import es.thinkingmachin.linksight.imatch.matcher.tree.AddressTreeNode;

import java.util.Arrays;

public class ReferenceMatch {
    public final AddressTreeNode match;
    public final double score;
    public final double[] scores;

    public ReferenceMatch(AddressTreeNode match, double score, double[] scores) {
        this.match = match;
        this.score = score;
        this.scores = scores;
    }

    @Override
    public String toString() {
        return match.toString() + ", final score: " + score + ", all scores: "+ Arrays.toString(scores);
    }
}
