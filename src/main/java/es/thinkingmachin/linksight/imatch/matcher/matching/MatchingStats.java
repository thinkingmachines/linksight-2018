package es.thinkingmachin.linksight.imatch.matcher.matching;

import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.LongAccumulator;
import java.util.concurrent.atomic.LongAdder;

public class MatchingStats {

    public final LongAdder totalCount = new LongAdder();
    public final LongAdder nullCount = new LongAdder();
    public final LongAdder brgyLevelCount = new LongAdder();
    public final LongAdder score075Count = new LongAdder();
    public final LongAdder score095Count = new LongAdder();
    public final LongAdder score100Count = new LongAdder();

    public void addNewMatch(ReferenceMatch match) {
        totalCount.increment();
        if (match == null) {
            nullCount.increment();
        } else {
            if (match.scores.length == 3)  brgyLevelCount.increment();
            if (match.score >= 0.75) score075Count.increment();
            if (match.score >= 0.95) score095Count.increment();
            if (match.score == 1) score100Count.increment();
        }
    }

    public void printStats() {
        System.out.println("Evaluation:");
        System.out.println("\tTotal: " + totalCount.longValue());
        printStat("Null", nullCount.longValue());
        printStat("Score >= 0.75", score075Count.longValue());
        printStat("Score >= 0.95", score095Count.longValue());
        printStat("Score == 1.00", score100Count.longValue());
        printStat("Brgy Level", brgyLevelCount.longValue());
    }

    private void printStat(String name, long count) {
        System.out.println(String.format("\t%s: %d (%.3f%%)", name, count, count*100.0/totalCount.longValue()));
    }
}
