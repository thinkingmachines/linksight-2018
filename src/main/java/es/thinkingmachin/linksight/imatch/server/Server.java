package es.thinkingmachin.linksight.imatch.server;

import com.google.common.base.Throwables;
import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.dataset.PsgcDataset;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference;
import es.thinkingmachin.linksight.imatch.matcher.tree.matcher.TreeAddressMatcher;
import es.thinkingmachin.linksight.imatch.server.jobs.Job;
import es.thinkingmachin.linksight.imatch.server.jobs.LinkSightCsvMatchingJob;
import es.thinkingmachin.linksight.imatch.server.messaging.Request;
import es.thinkingmachin.linksight.imatch.server.messaging.Response;
import es.thinkingmachin.linksight.imatch.server.messaging.Response.SparkResponseTransformer;
import io.reactivex.BackpressureStrategy;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import io.reactivex.subjects.PublishSubject;
import spark.Spark;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

import static es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference.DEFAULT_PSGC_DATASET;
import static es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference.EXTRA_PSGC_DATASET;

public class Server {

    // Spark server
    private final Integer port;

    // Job handling
    private final PublishSubject<Job> jobQueue = PublishSubject.create();
    private final Set<String> submittedJobs = new HashSet<>();
    private final ConcurrentHashMap<String, Response> jobResults = new ConcurrentHashMap<>();
    private final Disposable mainProcessing;

    // Matcher
    public TreeReference reference;
    public TreeAddressMatcher addressMatcher;

    public Server(Integer port) throws IOException {
        this.port = port;
        this.reference = new TreeReference(new PsgcDataset[]{ DEFAULT_PSGC_DATASET, EXTRA_PSGC_DATASET });
        this.addressMatcher = new TreeAddressMatcher(this.reference);
        this.mainProcessing = jobQueue.toFlowable(BackpressureStrategy.BUFFER)
                .doOnNext(job -> submittedJobs.add(job.id))
                .observeOn(Schedulers.single())
                .subscribe(job -> jobResults.put(job.id, job.run()));
    }

    public void start() {
        if (port == null) throw new IllegalArgumentException("Please specify the port.");
        System.out.println("Using port: "+ port);
        Spark.port(port);

        // Set up routes
        Spark.post("/submit", this::onSubmitJob, new SparkResponseTransformer());
        Spark.get("/jobresult/:id", this::onGetJobResult, new SparkResponseTransformer());
        Spark.exception(Exception.class, this::onServerException);

        System.out.println("\nServer ready!");
    }

    private String onServerException(Exception e, spark.Request req, spark.Response res) {
        System.out.println("Error handling request: " + req.body());
        System.out.println("\tStack trace:" + Throwables.getStackTraceAsString(e));
        res.status(500);
        return Response.createFailed(e).toJson();
    }

    private Response onSubmitJob(spark.Request req, spark.Response res) {
        Request request = Request.fromJson(req.body());
        if (request == null) throw new RuntimeException("Received malformed JSON:\n" + req.body());
        Dataset dataset = new Dataset(request.csvPath, request.columns);
        jobResults.remove(request.id);
        jobQueue.onNext(new LinkSightCsvMatchingJob(request.id, addressMatcher, dataset));
        return Response.createInProgress();
    }

    private Response onGetJobResult(spark.Request req, spark.Response res) {
        String id = req.params("id");
        if (!jobResults.containsKey(id)) {
            if (!submittedJobs.contains(id)) {
                return Response.createFailed(new Exception("Unknown job ID "+id));
            }
            return Response.createInProgress();
        } else {
            return jobResults.get(id);
        }
    }
}
