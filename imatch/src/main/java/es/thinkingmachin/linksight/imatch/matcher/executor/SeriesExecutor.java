package es.thinkingmachin.linksight.imatch.matcher.executor;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.io.source.InputSource;

import java.util.function.Consumer;

/**
 * This class serves as the task executor for sequential processing.
 */
public class SeriesExecutor implements Executor {

    /**
     * Executes threads sequentially.
     * @param source the source data
     * @param task the process to be run
     */
    @Override
    public void execute(InputSource source, Consumer<Address> task) {
        source.stream().forEachOrdered(task);
    }
}
