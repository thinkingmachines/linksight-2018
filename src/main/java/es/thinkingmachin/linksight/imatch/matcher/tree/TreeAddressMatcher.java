package es.thinkingmachin.linksight.imatch.matcher.tree;

import com.google.common.collect.Ordering;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.core.Interlevel;
import es.thinkingmachin.linksight.imatch.matcher.matchers.AddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import io.reactivex.annotations.NonNull;
import io.reactivex.annotations.Nullable;
import org.apache.commons.math3.util.Pair;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;

public class TreeAddressMatcher implements AddressMatcher {

    private TreeReference reference;

    public TreeAddressMatcher(TreeReference reference) {
        this.reference = reference;
    }

    @Nullable
    @Override
    public ReferenceMatch getTopMatch(Address address) {
        if (address.terms.length == 0) return null;
        List<ReferenceMatch> matches = getTopMatches(address, 1);
        if (matches.isEmpty()) return null;
        return matches.get(0);
    }

    @Override
    public List<ReferenceMatch> getTopMatches(Address address, int numMatches) {
        List<BfsTraversed> candidates = getCandidateMatches(address);
        List<BfsTraversed> bestN = Ordering.natural().greatestOf(candidates, numMatches);

        return bestN.stream()
                .filter(b -> b.node.getReferenceRow() != null)
                .map(b -> new ReferenceMatch(b.node.getReferenceRow(), b.overallScore))
                .collect(Collectors.toList());
    }

    private static double getOverallScore(double[] scores) {
        return Arrays.stream(scores).average().getAsDouble();
    }

    private LinkedList<BfsTraversed> getCandidateMatches(Address address) {
        LinkedList<BfsTraversed> possibleMatches = new LinkedList<>();
        LinkedList<BfsTraversed> queue = new LinkedList<>();
        queue.add(new BfsTraversed(reference.root, 0, null));

        // BFS
        BfsTraversed curNode;
        while (!queue.isEmpty()) {
            curNode = queue.removeFirst();

            int curNodeLevel = (curNode.node.level == null) ? Interlevel.values().length : curNode.node.level.ordinal();
            Interlevel childNodeLevel = Interlevel.indexed[curNodeLevel - 1];
            String term = address.getTermAtLevel(childNodeLevel);
            if (term == null) return new LinkedList<>(); // TODO: Handle skipped interlevel

            List<String> transformedTerms = getTransformedTerms(term);
            List<Pair<AddressTreeNode, Double>> fuzzyChildren = new LinkedList<>();
            for (String t : transformedTerms) {
                fuzzyChildren.addAll(curNode.node.fuzzyStringMap.getFuzzy(t));
            }

            for (Pair<AddressTreeNode, Double> fuzzyChild : fuzzyChildren) {
                AddressTreeNode childNode = fuzzyChild.getKey();
                double childScore = fuzzyChild.getValue();
                BfsTraversed bfsTraversed = new BfsTraversed(childNode, childScore, curNode);

                // Enqueue children
                if (childNodeLevel.ordinal() > address.minLevel.ordinal()) {
                    queue.add(bfsTraversed);
                }

                // Add to possible matches
                if (childNodeLevel.ordinal() == address.minLevel.ordinal()) {
                    possibleMatches.add(bfsTraversed);
                }
            }
        }
        return possibleMatches;
    }

    private static List<String> getTransformedTerms(String term) {
        LinkedList<String> terms = new LinkedList<>();
        terms.add(term);
        String[] words = term.split("[\\s@&.?$+-]+");
        if (words.length > 1) {
            terms.addAll(Arrays.asList(words));
        }
        for (int i = 0; i < words.length - 1; i++) {
            terms.add(words[i]+" "+words[i+1]);
        }
        return terms;
    }

    private static class BfsTraversed implements Comparable<BfsTraversed> {

        final AddressTreeNode node;
        final double[] scores;
        final double overallScore;

        BfsTraversed(AddressTreeNode node, double score, BfsTraversed parent) {
            this.node = node;
            if (parent != null) {
                scores = Arrays.copyOf(parent.scores, parent.scores.length + 1);
                scores[parent.scores.length] = score;
            } else {
                scores = new double[0];
            }
            this.overallScore = scores.length > 0 ? getOverallScore(scores) : 0;
        }


        @Override
        public int compareTo(BfsTraversed other) {
            double diff = this.overallScore - other.overallScore;
            if (diff > 0) {
                return 1;
            } else if (diff < 0) {
                return -1;
            }
            return 0;
        }
    }
}
