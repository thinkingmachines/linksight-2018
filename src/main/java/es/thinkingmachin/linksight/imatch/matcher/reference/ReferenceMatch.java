package es.thinkingmachin.linksight.imatch.matcher.reference;

import java.util.LinkedList;

public class ReferenceMatch {
    public final ReferenceRow referenceRow;
    public final double score;

    public ReferenceMatch(ReferenceRow referenceRow, double score) {
        this.referenceRow = referenceRow;
        this.score = score;
    }

    @Override
    public String toString() {
        return referenceRow.toString() + " score: " + score;
    }
}
