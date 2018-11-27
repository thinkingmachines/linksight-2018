package es.thinkingmachin.linksight.imatch.matcher.executor;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.io.source.InputSource;

import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ForkJoinPool;
import java.util.function.Consumer;
import java.util.stream.Collectors;

/**
 * This class serves as the task executor for parallel processing.
 */
public class ParallelExecutor implements Executor {

    /**
     * Executes threads in parallel.
     * @param source the source data
     * @param task the process to be run
     */
    @Override
    public void execute(InputSource source, Consumer<Address> task) {
        List<Address> all = source.stream().collect(Collectors.toList());

        ForkJoinPool customThreadPool = new ForkJoinPool(3);
        try {
            customThreadPool.submit(() -> all.parallelStream().forEachOrdered(task)).get();
        } catch (InterruptedException | ExecutionException e) {
            throw new Error(e);
        }

//        all.forEach(task);
    }
}