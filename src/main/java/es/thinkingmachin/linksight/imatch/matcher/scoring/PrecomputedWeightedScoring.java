package es.thinkingmachin.linksight.imatch.matcher.scoring;

import es.thinkingmachin.linksight.imatch.matcher.reference.Reference;
import org.apache.commons.collections4.map.LRUMap;

import java.util.Map;

public class PrecomputedWeightedScoring extends WeightedScoring {

    private final Reference reference;
    private final LRUMap<String, Map<String, Double>> cache;

    public PrecomputedWeightedScoring(Reference reference) {
        this.reference = reference;
        this.cache = new LRUMap<>(10000);
    }

    @Override
    public double getSimilarity(String search, String candidate) {
        if (!cache.containsKey(search)) {
            cache.put(search, reference.getCandidatesDictionary(search));
        }
        Map<String, Double> candidates = cache.get(search);
        return candidates.getOrDefault(candidate, 0.0) * 100.0;
    }

    @Override
    public double getAbsenceScore() {
        return 50;
    }
}
