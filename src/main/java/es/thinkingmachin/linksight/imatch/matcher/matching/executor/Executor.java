package es.thinkingmachin.linksight.imatch.matcher.matching.executor;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.io.source.InputSource;

import java.util.function.Consumer;

public interface Executor {

    void execute(InputSource source, Consumer<Address> task);
}
