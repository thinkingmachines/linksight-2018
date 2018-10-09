package es.thinkingmachin.linksight.imatch.server;

import com.google.common.base.Throwables;
import de.siegmar.fastcsv.writer.CsvAppender;
import de.siegmar.fastcsv.writer.CsvWriter;
import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.matchers.DatasetMatcher;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeAddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference;
import es.thinkingmachin.linksight.imatch.server.jobs.CsvMatchingJob;
import es.thinkingmachin.linksight.imatch.server.jobs.Job;
import es.thinkingmachin.linksight.imatch.server.messaging.Request;
import es.thinkingmachin.linksight.imatch.server.messaging.Response;
import io.reactivex.BackpressureStrategy;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import io.reactivex.subjects.PublishSubject;
import org.zeromq.ZMQ;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

public class Server {

    // ZeroMQ
    private final String ipcPath;

    // Job handling
    private final PublishSubject<Job> jobQueue = PublishSubject.create();
    private final ConcurrentHashMap<String, Response> jobResults = new ConcurrentHashMap<>();
    private final Disposable mainProcessing;

    // Matcher
    public TreeReference reference;
    public DatasetMatcher matcher;

    public Server(String ipcPath) throws IOException {
        this.ipcPath = ipcPath;
        this.reference = new TreeReference(TreeReference.DEFAULT_REF_DATASET);
        this.matcher = new DatasetMatcher(new TreeAddressMatcher(this.reference));
        this.mainProcessing = jobQueue.toFlowable(BackpressureStrategy.BUFFER)
                .observeOn(Schedulers.single())
                .subscribe(job -> jobResults.put(job.id, job.run()));
    }

    public void start() {
        ZMQ.Context context = ZMQ.context(1);
        ZMQ.Socket socket = context.socket(ZMQ.REP);
        socket.bind(ipcPath);

        while (true) {
            String received = socket.recvStr(Charset.defaultCharset());
            try {
                socket.send(handleRequest(received).toJson());
            } catch (Throwable e) {
                System.out.println("Error handling request: "+received);
                System.out.println("\tStack trace:" + Throwables.getStackTraceAsString(e));
                socket.send(Response.createFailed(e).toJson());
            }
        }
    }

    private Response handleRequest(String message) {
        Request request = Request.fromJson(message);
        if (request == null) {
            throw new RuntimeException("Received malformed JSON: "+message);
        }
        switch (request.type) {
            case SUBMIT_JOB:
                Dataset dataset = new Dataset(request.csvPath, request.columns);
                jobResults.remove(request.id);
                jobQueue.onNext(new CsvMatchingJob(request.id, matcher, dataset));
                return Response.createInProgress();
            case GET_JOB_RESULT:
                if (!jobResults.containsKey(request.id)) {
                    return Response.createInProgress();
                } else {
                    return jobResults.get(request.id);
                }
            default:
                throw new NotImplementedException();
        }
    }

    private static void writeOutput(List<ReferenceMatch> matches, String filePath) throws IOException {
        File file = new File(filePath);
        CsvWriter csvWriter = new CsvWriter();

        try (CsvAppender csvAppender = csvWriter.append(file, StandardCharsets.UTF_8)) {
            // Header
            csvAppender.appendLine("brgy", "municity", "prov", "score");
            // Values
            for (ReferenceMatch match : matches) {
                String[] terms;
                if (match == null) {
                    terms = new String[0];
                } else {
                    assert match.referenceRow != null;
                    assert match.referenceRow.stdAddress != null;
                    terms = match.referenceRow.stdAddress.terms;
                }
                assert terms.length <= 3;
                for (int i = 0; i < 3 - terms.length; i++) {
                    csvAppender.appendField("");
                }
                for (String term : terms) {
                    csvAppender.appendField(term);
                }
                if (match != null) {
                    csvAppender.appendField(String.format("%.2f", match.score));
                } else {
                    csvAppender.appendField("");
                }
                csvAppender.endLine();
            }
        }
    }
}
