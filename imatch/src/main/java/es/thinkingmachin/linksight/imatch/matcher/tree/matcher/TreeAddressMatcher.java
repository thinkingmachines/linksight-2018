package es.thinkingmachin.linksight.imatch.matcher.tree.matcher;

import com.google.common.collect.Ordering;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.core.Util;
import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.executor.Executor;
import es.thinkingmachin.linksight.imatch.matcher.executor.SeriesExecutor;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.ListSink;
import es.thinkingmachin.linksight.imatch.matcher.io.source.CsvSource;
import es.thinkingmachin.linksight.imatch.matcher.matching.AddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.matching.DatasetMatchingTask;
import es.thinkingmachin.linksight.imatch.matcher.model.FuzzyStringMap;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import es.thinkingmachin.linksight.imatch.matcher.tree.AddressTreeNode;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference;
import io.reactivex.annotations.NonNull;
import org.apache.commons.math3.util.Pair;

import java.util.*;
import java.util.stream.Collectors;

import static es.thinkingmachin.linksight.imatch.matcher.matching.DatasetMatchingTask.MatchesType.SINGLE;

/**
 * This class performs the matching algorithm to the reference tree.
 */
public class TreeAddressMatcher implements AddressMatcher {

    private TreeReference reference;

    public TreeAddressMatcher(TreeReference reference) {
        this.reference = reference;
        doWarmUps();
    }

    /**
     * Runs the matching algorithm once.
     * This would place the reference tree inside the cache which would
     * make the speed consistent across all datasets.
     * This method is called at the beginning of the program.
     */
    private void doWarmUps() {
        CsvSource source = new CsvSource(TestDataset.BuiltIn.FUZZY_200);
        ListSink sink = new ListSink();
        Executor executor = new SeriesExecutor();
        DatasetMatchingTask task = new DatasetMatchingTask(source, sink, executor, this, SINGLE);
        try {
            task.run(false);
            System.out.println("\nWarm-up done!\n");
        } catch (Throwable e) {
            System.out.println("Error warming up matcher: " + e.getMessage());
        }
    }

    /**
     * Gets the top matches returned by the matching algorithm
     * @param address       the address to be processed
     * @param numMatches    the number of matches to be used
     * @return a list of the top N matches
     */
    @NonNull
    @Override
    public List<ReferenceMatch> getTopMatches(Address address, int numMatches) {
        if (address.terms.length == 0) return Collections.emptyList();

        List<BfsTraversed> candidates = getCandidateMatches(createSearchStrings(address.terms, false), 0.95, reference.entryPoint);
        if (candidates.isEmpty()) candidates = getCandidateMatches(createSearchStrings(address.terms, true), 0, reference.muniCityEntryPoint);

        List<BfsTraversed> bestN = Ordering.from(BfsTraversed.createComparator())
                .greatestOf(candidates, numMatches);

        return bestN.stream()
                .map(b -> new ReferenceMatch(b.node, b.overallScore, b.scores))
                .collect(Collectors.toList());
    }

    /**
     * Performs the matching algorithm using breadth-first search.
     * It uses substrings from the search term and matches it with entries
     * inside the reference tree using PreDict.
     * @param searchStrings the substrings of the search term
     * @param scoreFilter   the minimum score a match should achieve
     * @return the final BFS queue entries
     */
    private LinkedList<BfsTraversed> getCandidateMatches(List<String>[] searchStrings, double scoreFilter, AddressTreeNode entryPoint) {
        LinkedList<BfsTraversed> possibleMatches = new LinkedList<>();
        LinkedList<BfsTraversed> queue = new LinkedList<>();
        queue.add(new BfsTraversed(entryPoint, 0, null, searchStrings));

        // BFS
        BfsTraversed curNode;
        while (!queue.isEmpty()) {
            curNode = queue.removeFirst();

            // Current node properties
            FuzzyStringMap<AddressTreeNode> fuzzyMap = curNode.node.childIndex.namesFuzzyMap;
            int aliasMaxWords = Math.min(curNode.node.maxChildAliasWords, 5);

            // For each phrase in remainingTerms
            for (int i = 0; i < curNode.remainingTerms.length; i++) {
                List<String> phrase = curNode.remainingTerms[i];
                int termsInPhrase = phrase.size();

                // Get sub-phrases of current phrase
                // j: first word of sub-phrase, k: last word of sub-phrase
                for (int j = 0; j < termsInPhrase; j++) {
                    // k is normally limited to termsInPhrase, but we also limit it to (j + aliasMaxWords) for speedup
                    int kLim = Math.min(termsInPhrase, j + aliasMaxWords);
                    for (int k = j + 1; k <= kLim; k++) {
                        String subPhrase = String.join(" ", phrase.subList(j, k));

                        // Get BFS children
                        Set<Pair<AddressTreeNode, Double>> fuzzyChildren = fuzzyMap.getFuzzy(subPhrase);

                        // Traverse each BFS child
                        for (Pair<AddressTreeNode, Double> fuzzyChild : fuzzyChildren) {
                            AddressTreeNode childNode = fuzzyChild.getKey();
                            double childScore = fuzzyChild.getValue();

                            // Create new remainingTerms object for child
                            List<String>[] newRemainingTerms = curNode.remainingTerms.clone();
                            LinkedList<String> newList = new LinkedList<>(phrase);
                            newList.subList(j, k).clear();
                            newRemainingTerms[i] = newList;

                            // The traversed child object
                            BfsTraversed bfsTraversed = new BfsTraversed(childNode, childScore, curNode, newRemainingTerms);

                            // Enqueue (BFS) if child has children
                            if (childNode.hasChildren()) {
                                queue.add(bfsTraversed);
                            }

                            // Add to possible matches
                            if (bfsTraversed.overallScore >= scoreFilter) {
                                possibleMatches.add(bfsTraversed);
                            }
                        }
                    }
                }
            }
        }
        return possibleMatches;
    }

    /**
     * Creates search strings to compare to in the fuzzy matching algorithm
     * @param locValues     the source location by interlevel
     * @param splitTerms    true if terms will be split by the specified delimiter
     * @return a list of substrings
     */
    @SuppressWarnings("unchecked")
    private List<String>[] createSearchStrings(String[] locValues, boolean splitTerms) {
        List<String>[] searchStrings = new List[locValues.length];
        for (int i = 0; i < locValues.length; i++) {
            if (splitTerms) {
                String[] words = Util.splitTerm(locValues[i]);
                searchStrings[i] = Arrays.asList(words);
            } else {
                searchStrings[i] = Collections.singletonList(locValues[i]);
            }
        }
        return searchStrings;
    }
}
