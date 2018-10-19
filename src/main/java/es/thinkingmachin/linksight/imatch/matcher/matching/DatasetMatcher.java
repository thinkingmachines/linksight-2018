package es.thinkingmachin.linksight.imatch.matcher.matching;

import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.OutputSink;
import es.thinkingmachin.linksight.imatch.matcher.io.source.InputSource;
import es.thinkingmachin.linksight.imatch.matcher.matching.executor.Executor;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.io.IOException;
import java.util.ArrayList;

@Deprecated
public class DatasetMatcher {

    private final AddressMatcher addressMatcher;

    public DatasetMatcher(AddressMatcher addressMatcher) {
        this.addressMatcher = addressMatcher;
    }

    @Deprecated
    public ArrayList<ReferenceMatch> getTopMatches(Dataset dataset) throws IOException {
        throw new NotImplementedException();
    }

    @Deprecated
    public void getPossibleMatches(InputSource source, OutputSink sink, Executor executor) throws IOException {
        throw new NotImplementedException();
    }
}
