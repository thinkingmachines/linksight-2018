package es.thinkingmachin.linksight.imatch.matcher.tree;

import com.google.common.collect.Ordering;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.core.Util;
import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.executor.Executor;
import es.thinkingmachin.linksight.imatch.matcher.executor.ParallelExecutor;
import es.thinkingmachin.linksight.imatch.matcher.executor.SeriesExecutor;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.ListSink;
import es.thinkingmachin.linksight.imatch.matcher.io.source.CsvSource;
import es.thinkingmachin.linksight.imatch.matcher.matching.AddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.matching.DatasetMatchingTask;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import io.reactivex.annotations.NonNull;
import io.reactivex.annotations.Nullable;
import org.apache.commons.math3.util.Pair;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

import static es.thinkingmachin.linksight.imatch.matcher.matching.DatasetMatchingTask.MatchesType.SINGLE;

public class TreeAddressMatcher implements AddressMatcher {

    private TreeReference reference;

    public TreeAddressMatcher(TreeReference reference) {
        this.reference = reference;
    }

    public void warmUp() {
        CsvSource source = new CsvSource(TestDataset.BuiltIn.FUZZY_200);
        ListSink sink = new ListSink();
        Executor executor =  new SeriesExecutor();
        DatasetMatchingTask task = new DatasetMatchingTask(source, sink, executor, this, SINGLE);
        try {
            task.run(false);
            System.out.println("\nWarm-up done!\n");
        } catch (Throwable e) {
            System.out.println("Error warming up matcher: "+e.getMessage());
        }
    }

    @Nullable
    @Override
    public ReferenceMatch getTopMatch(Address address) {
        if (address.terms.length == 0) return null;
        List<ReferenceMatch> matches = getTopMatches(address, 1);
        if (matches.isEmpty()) return null;
        return matches.get(0);
    }

    @NonNull
    @Override
    public List<ReferenceMatch> getTopMatches(Address address, int numMatches) {
        if (address.terms.length == 0) return Collections.emptyList();

        List<BfsTraversed> candidates = getCandidateMatches(address.terms, true);
        if (candidates.isEmpty()) candidates = getCandidateMatches(address.terms, false);

        List<BfsTraversed> bestN = Ordering.from(BfsTraversed.createComparator())
                .greatestOf(candidates, numMatches);

        return bestN.stream()
                .map(b -> new ReferenceMatch(b.node, b.overallScore, b.scores))
                .collect(Collectors.toList());
    }


    private LinkedList<BfsTraversed> getCandidateMatches(String[] locValues, boolean optimized) {
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
                forEachTerm: for (int j = 0; j < numTerms; j++) {
                    for (int k = j + 1; k <= Math.min(j + aliasMaxWords, numTerms); k++) {
                        if (optimized) {
                            k = numTerms;
                        }
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
                            if (optimized && bfsTraversed.overallScore < 0.95) {
                                continue;
                            }
                            possibleMatches.add(bfsTraversed);
                        }
                        if (optimized) break forEachTerm;
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
