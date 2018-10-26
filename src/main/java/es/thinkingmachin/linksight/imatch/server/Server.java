package es.thinkingmachin.linksight.imatch.server;

import com.google.common.base.Throwables;
import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.dataset.PsgcDataset;
import es.thinkingmachin.linksight.imatch.matcher.tree.matcher.TreeAddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference;
import es.thinkingmachin.linksight.imatch.server.jobs.LinkSightCsvMatchingJob;
import es.thinkingmachin.linksight.imatch.server.jobs.Job;
import es.thinkingmachin.linksight.imatch.server.messaging.Request;
import es.thinkingmachin.linksight.imatch.server.messaging.Response;
import io.reactivex.BackpressureStrategy;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import io.reactivex.subjects.PublishSubject;
import org.zeromq.ZMQ;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.io.IOException;
import java.nio.charset.Charset;
import java.util.concurrent.ConcurrentHashMap;

import static es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference.DEFAULT_PSGC_DATASET;
import static es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference.EXTRA_PSGC_DATASET;

public class Server {

    // ZeroMQ
    private final String ipcPath;

    // Job handling
    private final PublishSubject<Job> jobQueue = PublishSubject.create();
    private final ConcurrentHashMap<String, Response> jobResults = new ConcurrentHashMap<>();
    private final Disposable mainProcessing;

    // Matcher
    public TreeReference reference;
    public TreeAddressMatcher addressMatcher;

    public Server(String ipcPath) throws IOException {
        this.ipcPath = ipcPath;
        this.reference = new TreeReference(new PsgcDataset[]{ DEFAULT_PSGC_DATASET, EXTRA_PSGC_DATASET });
        this.addressMatcher = new TreeAddressMatcher(this.reference);
        this.mainProcessing = jobQueue.toFlowable(BackpressureStrategy.BUFFER)
                .observeOn(Schedulers.single())
                .subscribe(job -> jobResults.put(job.id, job.run()));
    }

    public void start() {
        if (ipcPath == null) throw new IllegalArgumentException("Please specify the IPC path.");
        System.out.println("Using IPC path: "+ipcPath);
        ZMQ.Context context = ZMQ.context(1);
        ZMQ.Socket socket = context.socket(ZMQ.REP);
        socket.bind(ipcPath);
        System.out.println("\nServer ready!");

        while (true) {
            String received = socket.recvStr(Charset.defaultCharset());
            try {
                socket.send(handleRequest(received).toJson());
            } catch (Throwable e) {
                System.out.println("Error handling request: " + received);
                System.out.println("\tStack trace:" + Throwables.getStackTraceAsString(e));
                socket.send(Response.createFailed(e).toJson());
            }
        }
    }

    private Response handleRequest(String message) {
        Request request = Request.fromJson(message);
        System.out.println("Received message: "+message);
        if (request == null) {
            throw new RuntimeException("Received malformed JSON: " + message);
        }
        switch (request.type) {
            case SUBMIT_JOB:
                Dataset dataset = new Dataset(request.csvPath, request.columns);
                jobResults.remove(request.id);
                jobQueue.onNext(new LinkSightCsvMatchingJob(request.id, addressMatcher, dataset));
                return Response.createInProgress();
            case GET_JOB_RESULT:
                System.out.println("Sent Response");
                if (!jobResults.containsKey(request.id)) {
                    return Response.createInProgress();
                } else {
                    return jobResults.get(request.id);
                }
            default:
                throw new NotImplementedException();
        }
    }
}
