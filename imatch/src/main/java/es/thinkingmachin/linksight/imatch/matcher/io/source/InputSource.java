package es.thinkingmachin.linksight.imatch.matcher.io.source;


import es.thinkingmachin.linksight.imatch.matcher.core.Address;

import java.io.IOException;
import java.util.Iterator;
import java.util.Spliterator;
import java.util.Spliterators;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

/**
 * This class serves as the interface for all input files and sources.
 */
public interface InputSource extends Iterator<Address> {

    void open() throws IOException;

    boolean close();

    int getCurrentCount();

    String getName();

    default Stream<Address> stream() {
        Spliterator<Address> spl = Spliterators.spliteratorUnknownSize(this, Spliterator.ORDERED);
        return StreamSupport.stream(spl, false);
    }
}
