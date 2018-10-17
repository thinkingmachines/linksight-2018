package es.thinkingmachin.linksight.imatch.matcher.tree;

import com.google.common.collect.Ordering;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.core.Util;
import es.thinkingmachin.linksight.imatch.matcher.matchers.AddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import io.reactivex.annotations.Nullable;
import org.apache.commons.math3.util.Pair;

import java.util.*;
import java.util.stream.Collectors;

public class TreeAddressMatcher implements AddressMatcher {

    private TreeReference reference;

    public TreeAddressMatcher(TreeReference reference) {
        this.reference = reference;
    }

    @Nullable
    @Override
    public ReferenceMatch getTopMatch(Address address, CsvRow row) {
        if (address.terms.length == 0) return null;
        List<ReferenceMatch> matches = getTopMatches(address, 1, row);
        if (matches.isEmpty()) return null;
        return matches.get(0);
    }

    @Override
    public List<ReferenceMatch> getTopMatches(Address address, int numMatches, CsvRow row) {
        List<BfsTraversed> candidates = getCandidateMatches(address.terms, row);
        List<BfsTraversed> bestN = Ordering.from(BfsTraversed.createComparator())
                .greatestOf(candidates, numMatches);

        return bestN.stream()
                .map(b -> new ReferenceMatch(b.node, b.overallScore, b.scores))
                .collect(Collectors.toList());
    }

    private LinkedList<BfsTraversed> getCandidateMatches(String[] locValues, CsvRow row) {
        List<String>[] searchStrings = createSearchStrings(locValues);
        LinkedList<BfsTraversed> possibleMatches = new LinkedList<>();
        LinkedList<BfsTraversed> queue = new LinkedList<>();
        queue.add(new BfsTraversed(reference.entryPoint, 0, null, searchStrings));

        // BFS
        BfsTraversed curNode;
        while (!queue.isEmpty()) {
            curNode = queue.removeFirst();

            int aliasMaxWords = curNode.node.maxChildAliasWords;
            for (int i = 0; i < curNode.remainingTerms.length; i++) {
                List<String> locValue = curNode.remainingTerms[i];
                int numTerms = locValue.size();
                for (int j = 0; j < numTerms; j++) {
                    for (int k = j + 1; k <= Math.min(j + aliasMaxWords, numTerms); k++) {
                        String candidate = String.join(" ",locValue.subList(j, k));
                        Set<Pair<AddressTreeNode, Double>> fuzzyChildren = curNode.node.childIndex.namesFuzzyMap.getFuzzy(candidate);
                        for (Pair<AddressTreeNode, Double> fuzzyChild : fuzzyChildren) {
                            AddressTreeNode childNode = fuzzyChild.getKey();
                            double childScore = fuzzyChild.getValue();// * BfsTraversed.getWordCoverageScore(numTerms - k + j);
//                            if (row.getOriginalLineNumber() == 1089) {
//                                System.out.println("Child node: "+childNode.getOrigTerm()+" score: "+childScore+", candidate: "+candidate+" jk: "+j+","+k);
//                                System.out.println("- Cur node: "+curNode.node.getOrigTerm());
//                                System.out.println("- Num terms: "+numTerms);
//                            }

                            List<String>[] newRemainingTerms = curNode.remainingTerms.clone();
                            LinkedList<String> newList = new LinkedList<>(locValue);
                            newList.subList(j, k).clear();
                            newRemainingTerms[i] = newList;
                            BfsTraversed bfsTraversed = new BfsTraversed(childNode, childScore, curNode, newRemainingTerms);

                            // Enqueue (BFS) if child has children
                            if (childNode.hasChildren()) {
                                queue.add(bfsTraversed);
                            }

                            // Add to possible matches
                            possibleMatches.add(bfsTraversed);
                        }
                    }
                }
            }
        }
//        if (true) {
//            System.out.println(possibleMatches);
//            throw new Error();
//        }
        return possibleMatches;
    }

    private List<String>[] createSearchStrings(String[] locValues) {
        List<String>[] searchStrings = new List[locValues.length];
        for (int i = 0;  i < locValues.length; i++) {
            String[] words = Util.splitTerm(locValues[i]);
            searchStrings[i] = Arrays.asList(words);
        }
        return searchStrings;
    }

    private static class BfsTraversed {

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

        @Override
        public String toString() {
            return "BfsTraversed{" +
                    "node=" + node +
                    ", scores=" + Arrays.toString(scores) +
                    ", overallScore=" + overallScore +
                    '}';
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
}
