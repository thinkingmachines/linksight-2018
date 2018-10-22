package es.thinkingmachin.linksight.imatch.matcher.executor;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.io.source.InputSource;

import java.util.function.Consumer;

public class SeriesExecutor implements Executor {

    @Override
    public void execute(InputSource source, Consumer<Address> task) {
        source.stream().forEachOrdered(task);
    }
}
