package es.thinkingmachin.linksight.imatch.matcher.matching;

import com.google.common.base.Stopwatch;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.OutputSink;
import es.thinkingmachin.linksight.imatch.matcher.io.source.InputSource;
import es.thinkingmachin.linksight.imatch.matcher.matching.executor.Executor;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import es.thinkingmachin.linksight.imatch.server.jobs.Job;
import es.thinkingmachin.linksight.imatch.server.messaging.Response;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class DatasetMatchingTask {

    private final InputSource inputSource;
    private final OutputSink outputSink;
    private final Executor executor;
    private final AddressMatcher addressMatcher;
    private final MatchesType matchesType;

    public DatasetMatchingTask(InputSource inputSource, OutputSink outputSink, Executor executor,
                               AddressMatcher addressMatcher, MatchesType matchesType) {
        this.inputSource = inputSource;
        this.outputSink = outputSink;
        this.executor = executor;
        this.addressMatcher = addressMatcher;
        this.matchesType = matchesType;
    }

    public void run() throws Throwable {
        try {
            System.out.println("Starting matching...");
            Stopwatch stopwatch = Stopwatch.createStarted();
            inputSource.open();
            outputSink.open();
            executor.execute(inputSource, this::matchAddress);
            stopwatch.stop();
            long duration = stopwatch.elapsed(TimeUnit.MILLISECONDS);
            System.out.println("Matching took " + (duration / 1000.0) + " sec at " + (outputSink.getSize() * 1000.0 / duration) + " rows/sec.");
        } catch (Throwable e) {
            cleanup();
            throw e;
        }
        cleanup();
    }

    private void cleanup() {
        inputSource.close();
        outputSink.close();
    }

    private void matchAddress(Address address) {
        long startTime = System.nanoTime();
        List<ReferenceMatch> matches = addressMatcher.getTopMatches(address, matchesType.numMatches);
        double matchTime = (System.nanoTime() - startTime) / 1e9;
        for (ReferenceMatch match : matches) {
            try {
                outputSink.addMatch(address.rowNum, address, matchTime, match);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
    }

    public enum MatchesType {
        SINGLE(1),
        MULTIPLE(3);

        public int numMatches;

        MatchesType(int numMatches) {
            this.numMatches = numMatches;
        }
    }
}
