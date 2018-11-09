package es.thinkingmachin.linksight.imatch.matcher.tree.matcher;

import es.thinkingmachin.linksight.imatch.matcher.tree.AddressTreeNode;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

/**
 * This class encapsulates information on each entry in the BFS queue.
 * It includes information about the node, the array of scores, its overall score
 * and the remaining terms in the search strings to be compared.
 */
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

    /**
     * Computes for the overall score of the node using the scores of
     * the matched address per interlevel.
     * The overall score is computed by getting the average score
     * and multiplying it to the word coverage score.
     * @param scores    the array of scores per interlevel
     * @return the overall score
     */
    private double getOverallScore(double[] scores) {
        double avgScore = Arrays.stream(scores).average().getAsDouble();
        return avgScore * getWordCoverageScore(getTotalRemaining());
    }

    public static Comparator<BfsTraversed> createComparator() {
        return Comparator
                .comparingDouble(b -> b.overallScore);
    }

    /**
     * Get the total number of remaining search strings
     * @return the number of remaining search strings
     */
    public int getTotalRemaining() {
        int total = 0;
        for (List<String> l : remainingTerms) {
            total += l.size();
        }
        return total;
    }

    /**
     * Computes for the score of the remaining words in the search substrings
     * @param remainingWords the number of remaining words in the search strings
     * @return the word coverage score
     */
    static double getWordCoverageScore(int remainingWords) {
        return Math.max(Math.pow(0.9, remainingWords), 0.4);
    }
}