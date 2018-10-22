package es.thinkingmachin.linksight.imatch.matcher.tree.matcher;

import es.thinkingmachin.linksight.imatch.matcher.tree.AddressTreeNode;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public class BfsTraversed {

    final AddressTreeNode node;
    final double[] scores;
    final double overallScore;
    final List<String>[] remainingTerms;

    BfsTraversed(AddressTreeNode node, double score, BfsTraversed parent, List<String>[] remainingTerms) {
        this.node = node;
        this.remainingTerms = remainingTerms;
        if (parent != null) { // child
            scores = Arrays.copyOf(parent.scores, parent.scores.length + 1);
            scores[parent.scores.length] = score;
        } else { // parent
            scores = new double[0];
        }
        this.overallScore = scores.length > 0 ? getOverallScore(scores) : 0;
    }

    private double getOverallScore(double[] scores) {
        double avgScore = Arrays.stream(scores).average().getAsDouble();
        return avgScore * getWordCoverageScore(getTotalRemaining());
    }

    public static Comparator<BfsTraversed> createComparator() {
        return Comparator
                .comparingDouble(b -> b.overallScore);
    }

    public int getTotalRemaining() {
        int total = 0;
        for (List<String> l : remainingTerms) {
            total += l.size();
        }
        return total;
    }

    static double getWordCoverageScore(int remainingWords) {
        return Math.max(Math.pow(0.9, remainingWords), 0.4);
    }
}