package es.thinkingmachin.linksight.imatch.matcher.matching;

import com.google.common.base.Stopwatch;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.OutputSink;
import es.thinkingmachin.linksight.imatch.matcher.io.source.InputSource;
import es.thinkingmachin.linksight.imatch.matcher.executor.Executor;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * This class executes the dataset matching job.
 */
public class DatasetMatchingTask {

    private final InputSource inputSource;
    private final OutputSink outputSink;
    private final Executor executor;
    private final AddressMatcher addressMatcher;
    private final MatchesType matchesType;
    public final MatchingStats matchingStats;

    public DatasetMatchingTask(InputSource inputSource, OutputSink outputSink, Executor executor,
                               AddressMatcher addressMatcher, MatchesType matchesType) {
        this.inputSource = inputSource;
        this.outputSink = outputSink;
        this.executor = executor;
        this.addressMatcher = addressMatcher;
        this.matchesType = matchesType;
        this.matchingStats = new MatchingStats();
    }

    public void run() throws Throwable {
        run(true);
    }

    /**
     * Executes the matching task and prints out statistics.
     * @param verbose true if statistics will be displayed, false otherwise
     * @throws Throwable
     */
    public void run(boolean verbose) throws Throwable {
        try {
            if (verbose) System.out.println("Starting matching: "+inputSource.getName());
            Stopwatch stopwatch = Stopwatch.createStarted();
            inputSource.open();
            outputSink.open();
            executor.execute(inputSource, this::matchAddress);
            stopwatch.stop();
            long duration = stopwatch.elapsed(TimeUnit.MILLISECONDS);

            // Stats
            if (verbose) {
                System.out.println("Matching done:");
                System.out.println("- Time: " + (duration / 1000.0) + " sec");
                System.out.println(String.format("- Speed: %.3f rows/sec", inputSource.getCurrentCount() * 1000.0 / duration));
                System.out.println("- Output: " + outputSink.getName());
                System.out.println();
            }
        } catch (Throwable e) {
            cleanup();
            throw e;
        }
        cleanup();
    }

    /**
     * Closes the input reader and output writer
     */
    private void cleanup() {
        inputSource.close();
        outputSink.close();
    }

    /**
     * Runs the matching algorithm and computes for the matching statistics.
     * @param address   the input location to be searched against the reference tree
     */
    private void matchAddress(Address address) {
        long startTime = System.nanoTime();
        List<ReferenceMatch> matches = addressMatcher.getTopMatches(address, matchesType.numMatches);
        double matchTime = (System.nanoTime() - startTime) / 1e9;
        for (ReferenceMatch match : matches) {
            try {
                matchingStats.addNewMatch(match);
                long curCount = matchingStats.totalCount.longValue();
                if (curCount % 10000 == 0) {
                    System.out.println("Current count: "+curCount);
                }
                outputSink.addMatch(address.rowNum, address, matchTime, match);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
    }

    /**
     * Count of top matches that can be used.
     */
    public enum MatchesType {
        SINGLE(1),
        MULTIPLE(3);

        public int numMatches;

        MatchesType(int numMatches) {
            this.numMatches = numMatches;
        }
    }
}
