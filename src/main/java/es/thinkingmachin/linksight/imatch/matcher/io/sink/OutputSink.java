package es.thinkingmachin.linksight.imatch.matcher.io.sink;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.IOException;

public interface OutputSink {

    void open() throws IOException;

    default boolean close() {
        return true;
    }

    void addMatch(long index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException;

    int getSize();

    String getName();
}
