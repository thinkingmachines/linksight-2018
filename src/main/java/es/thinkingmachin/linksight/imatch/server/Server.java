package es.thinkingmachin.linksight.imatch.server;

import es.thinkingmachin.linksight.imatch.server.Lpserver;
import es.thinkingmachin.linksight.imatch.matcher.core.MatchingJob;
import es.thinkingmachin.linksight.imatch.matcher.reference.Reference;
import es.thinkingmachin.linksight.imatch.matcher.eval.Evaluator;

import java.io.IOException;

public class Server {

    // Reference
    private static String REF_CSV_PATH = "data/psgc-locations.csv";
    private static String[] REF_LOC_COLS = {"bgy", "municity", "prov"};
    private static String REF_PSGC_COL = "code";
    private static String REF_ALIAS_COL = "candidate_terms";

    // Test CSV
//    private static String TEST_CSV_PATH = "data/happy_path.csv";
    private static String TEST_CSV_PATH = "data/linksight-testing-file-fuzzy-200.csv";
    private static String[] TEST_LOC_COLS = {"source_brgy", "source_municity", "source_prov"};
    private static String[] TEST_CORRECT_COLS = {"expected_brgy", "expected_municity", "expected_prov"};

    public static void main(String[] args) throws Exception {
        System.out.println(getVersion());

        Lpserver.main(args);

        if (true) return;

        System.out.println("\nTest CSV: " + TEST_CSV_PATH + "\n");

        long startMem = getMemUsage();
        // Get es.thinkingmachin.linksight.imatch.matcher.reference file and create model
        Reference reference = new Reference(REF_CSV_PATH, REF_LOC_COLS, REF_PSGC_COL, REF_ALIAS_COL);
        System.out.println("After ref: "+(getMemUsage()-startMem));

        // Do matching on the test csv
        MatchingJob matchingJob = new MatchingJob(reference, TEST_CSV_PATH, TEST_LOC_COLS);
        matchingJob.start();

        System.out.println("After matching: "+(getMemUsage()-startMem));

        // Check accuracy
        Evaluator.evaluate(matchingJob.matchedRows, TEST_CSV_PATH, TEST_CORRECT_COLS);
    }

    private static long getMemUsage() {
        return Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
    }

    public static String getVersion() {
        return Server.class.getPackage().getImplementationVersion();
    }
}
