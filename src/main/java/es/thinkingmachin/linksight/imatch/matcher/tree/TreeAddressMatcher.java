package es.thinkingmachin.linksight.imatch.matcher.tree;

import com.google.common.collect.Ordering;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.matchers.AddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import io.reactivex.annotations.Nullable;
import org.apache.commons.math3.util.Pair;

import java.util.Arrays;
import java.util.Comparator;
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
        List<BfsTraversed> candidates = getCandidateMatches(address.terms);
        List<BfsTraversed> bestN = Ordering.from(BfsTraversed.createComparator())
                .greatestOf(candidates, numMatches);

        return bestN.stream()
                .map(b -> new ReferenceMatch(b.node, b.overallScore))
                .collect(Collectors.toList());
    }

    private LinkedList<BfsTraversed> getCandidateMatches(String[] searchStrings) {
        List<String> transformedTerms = getTransformedTerms(searchStrings);
        LinkedList<BfsTraversed> possibleMatches = new LinkedList<>();
        LinkedList<BfsTraversed> queue = new LinkedList<>();
        queue.add(new BfsTraversed(reference.entryPoint, 0, null));

        // BFS
        BfsTraversed curNode;
        while (!queue.isEmpty()) {
            curNode = queue.removeFirst();

            List<Pair<AddressTreeNode, Double>> fuzzyChildren = new LinkedList<>();
            for (String t : transformedTerms) {
                fuzzyChildren.addAll(curNode.node.childIndex.namesFuzzyMap.getFuzzy(t));
            }

            for (Pair<AddressTreeNode, Double> fuzzyChild : fuzzyChildren) {
                AddressTreeNode childNode = fuzzyChild.getKey();
                double childScore = fuzzyChild.getValue();
                BfsTraversed bfsTraversed = new BfsTraversed(childNode, childScore, curNode);

                // Enqueue (BFS) if child has children
                if (childNode.hasChildren()) {
                    queue.add(bfsTraversed);
                }

                // Add to possible matches
                possibleMatches.add(bfsTraversed);
            }
        }
//        if (true) {
//            System.out.println(possibleMatches);
//            throw new Error();
//        }
        return possibleMatches;
    }

    private static List<String> getTransformedTerms(String[] searchStrings) {
        LinkedList<String> terms = new LinkedList<>();
        for (String searchString : searchStrings) {
            terms.add(searchString);
            String[] words = searchString.split("[\\s@&.?$+-]+");
            if (words.length > 1) {
                terms.addAll(Arrays.asList(words));
            }
            for (int i = 0; i < words.length - 1; i++) {
                terms.add(words[i] + " " + words[i + 1]);
            }
        }
        return terms;
    }

    private static class BfsTraversed {

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

        private static double getOverallScore(double[] scores) {
            return Arrays.stream(scores).average().getAsDouble();
        }

        public static Comparator<BfsTraversed> createComparator() {
            return Comparator
                    .<BfsTraversed>comparingDouble(b -> b.scores.length)
                    .thenComparingDouble(b -> b.overallScore);
        }

        @Override
        public String toString() {
            return "BfsTraversed{" +
                    "node=" + node +
                    ", scores=" + Arrays.toString(scores) +
                    ", overallScore=" + overallScore +
                    '}';
        }
    }
}
