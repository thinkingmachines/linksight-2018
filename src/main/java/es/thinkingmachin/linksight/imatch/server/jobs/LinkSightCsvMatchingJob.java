package es.thinkingmachin.linksight.imatch.server.jobs;

import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.LinkSightCsvSink;
import es.thinkingmachin.linksight.imatch.matcher.io.source.CsvSource;
import es.thinkingmachin.linksight.imatch.matcher.matching.AddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.matching.DatasetMatchingTask;
import es.thinkingmachin.linksight.imatch.matcher.matching.executor.SeriesExecutor;
import es.thinkingmachin.linksight.imatch.server.messaging.Response;

public class LinkSightCsvMatchingJob extends Job {

    protected AddressMatcher addressMatcher;
    protected Dataset dataset;

    public LinkSightCsvMatchingJob(String id, AddressMatcher addressMatcher, Dataset dataset) {
        super(id);
        this.addressMatcher = addressMatcher;
        this.dataset = dataset;
    }

    @Override
    public Response run() {
        try {
            CsvSource source = new CsvSource(dataset);
            LinkSightCsvSink sink = new LinkSightCsvSink();
            DatasetMatchingTask task = new DatasetMatchingTask(source, sink, new SeriesExecutor(), addressMatcher, DatasetMatchingTask.MatchesType.MULTIPLE);
            task.run();
            return Response.createSuccess(sink.getOutputFile().getAbsolutePath());
        } catch (Throwable e) {
            System.out.println("Error running matching.");
            e.printStackTrace();
            return Response.createFailed(e);
        }
    }
}
