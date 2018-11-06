package es.thinkingmachin.linksight.imatch.matcher.executor;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.io.source.InputSource;

import java.util.function.Consumer;

/**
 * This class serves as the interface for all executor instances for matching addresses.
 */
public interface Executor {

    void execute(InputSource source, Consumer<Address> task);
}
