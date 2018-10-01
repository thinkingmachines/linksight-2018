package matchers;

import candidates.CandidatesFilter;
import candidates.FirstLevelCandidatesFilter;
import com.google.common.base.Stopwatch;
import core.Address;
import reference.ReferenceMatch;
import reference.Reference;
import reference.ReferenceRow;
import scoring.PrecomputedWeightedScoring;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class BasicMatcher {

    private final Reference reference;
    private final CandidatesFilter candidatesFilter;
    private final PrecomputedWeightedScoring scoring;

//    public static long METRIC_CANDIDATE_GEN_TOTAL = 0;
//    public static long METRIC_CANDIDATE_GEN_COUNT = 0;
//
//    public static long METRIC_TOP_MATCH_TOTAL = 0;
//    public static long METRIC_TOP_MATCH_COUNT = 0;

    public static ArrayList<Long> metricCandidateGen = new ArrayList<>(2000);
    public static ArrayList<Long> metricTopMatch = new ArrayList<>(2000);

    public BasicMatcher(Reference reference) {
        this.reference = reference;
        this.candidatesFilter = new FirstLevelCandidatesFilter(reference);
        this.scoring = new PrecomputedWeightedScoring(reference);
    }

    public ReferenceMatch getTopMatch(final Address search) {
        Stopwatch stopwatch = Stopwatch.createStarted();
        List<ReferenceRow> candidates = candidatesFilter.generate(search);
        stopwatch.stop();
        long duration = stopwatch.elapsed(TimeUnit.MICROSECONDS);
        if (duration >= 1E6) {
            System.out.println("**OUTLIER** Matcher candidate gen: "+search+", duration: "+duration);
        }
        metricCandidateGen.add(stopwatch.elapsed(TimeUnit.MICROSECONDS));


        stopwatch = Stopwatch.createStarted();
        double bestScore = -1;
        ReferenceMatch bestMatch = null;
        for (ReferenceRow candidateRef : candidates) {
            Address candidate = candidateRef.aliasAddress;
            candidate.cleanTerms(reference);
            double score = scoring.getScore(search, candidate);
            if (score > bestScore) {
                bestScore = score;
                bestMatch = new ReferenceMatch(candidateRef, score);
            }
        }

        stopwatch.stop();

        duration = stopwatch.elapsed(TimeUnit.MICROSECONDS);
        if (duration >= 1E6) {
            System.out.println("**OUTLIER** Top match: "+search+" size: "+candidates.size()+", duration: "+duration+", position: "+metricTopMatch.size());
        }
        metricTopMatch.add(duration);

        return bestMatch;
    }

}
