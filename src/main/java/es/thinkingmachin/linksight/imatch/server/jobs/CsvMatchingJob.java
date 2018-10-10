package es.thinkingmachin.linksight.imatch.server.jobs;

import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.matchers.DatasetMatcher;
import es.thinkingmachin.linksight.imatch.server.messaging.Response;

import java.io.File;

public class CsvMatchingJob extends Job {

    protected DatasetMatcher matcher;
    protected Dataset dataset;

    public CsvMatchingJob(String id, DatasetMatcher matcher, Dataset dataset) {
        super(id);
        this.matcher = matcher;
        this.dataset = dataset;
    }

    @Override
    public Response run() {
        try {
            File output = matcher.getPossibleMatches(dataset);
            return Response.createSuccess(output.getAbsolutePath());
        } catch (Throwable e) {
            System.out.println("Error running matching.");
            e.printStackTrace();
            return Response.createFailed(e);
        }
    }
}
