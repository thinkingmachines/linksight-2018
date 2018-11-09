package es.thinkingmachin.linksight.imatch.matcher.reference;

import es.thinkingmachin.linksight.imatch.matcher.tree.AddressTreeNode;

import java.util.Arrays;

/**
 * This class encapsulates the information about the matched value.
 * It includes information about the score for the match and the
 * list of scores for each interlevel.
 */
public class ReferenceMatch {
    public final AddressTreeNode match;
    public final double score;
    public final double[] scores;

    public ReferenceMatch(AddressTreeNode match, double score, double[] scores) {
        this.match = match;
        this.score = score;
        this.scores = scores;
    }

    /**
     * Converts to string the final score and the list of scores for each interlevel
     * @return string of the final score and the list of scores for each interlevel
     */
    @Override
    public String toString() {
        return match.toString() + ", final score: " + score + ", all scores: "+ Arrays.toString(scores);
    }
}
