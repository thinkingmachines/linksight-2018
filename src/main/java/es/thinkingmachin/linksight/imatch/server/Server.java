package es.thinkingmachin.linksight.imatch.server;

import es.thinkingmachin.linksight.imatch.matcher.dataset.ReferenceDataset;
import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.eval.Evaluator;
import es.thinkingmachin.linksight.imatch.matcher.matchers.DatasetMatcher;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeAddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference;

import java.util.List;
import java.util.zip.DataFormatException;

public class Server {

    // Reference
    private static ReferenceDataset referenceDataset = new ReferenceDataset(
            "data/psgc-locations.csv",
            new String[]{"bgy", "municity", "prov"},
            "code",
            "candidate_terms"
    );

    public static void main(String[] args) throws Exception {
        TestDataset testDataset = TestDataset.BuiltIn.FUZZY_200;

        TreeReference reference = new TreeReference(referenceDataset);
        DatasetMatcher matcher = new DatasetMatcher(new TreeAddressMatcher(reference));

        List<ReferenceMatch> matches = matcher.getTopMatches(testDataset);
        Evaluator.evaluate(matches, testDataset);

//        System.out.println(getVersion());
//
//        Lpserver.main(args);
//
//        if (true) return;
//
//        System.out.println("\nTest CSV: " + TEST_CSV_PATH + "\n");
//
//        long startMem = getMemUsage();
//        // Get es.thinkingmachin.linksight.imatch.matcher.reference file and create model
//        Reference reference = new Reference(REF_CSV_PATH, REF_LOC_COLS, REF_PSGC_COL, REF_ALIAS_COL);
//        System.out.println("After ref: "+(getMemUsage()-startMem));
//
//        // Do matching on the test csv
//        MatchingJob matchingJob = new MatchingJob(reference, TEST_CSV_PATH, TEST_LOC_COLS);
//        matchingJob.start();
//
//        System.out.println("After matching: "+(getMemUsage()-startMem));
//
//        // Check accuracy
//        Evaluator.evaluate(matchingJob.matchedRows, TEST_CSV_PATH, TEST_CORRECT_COLS);
    }

    private static long getMemUsage() {
        return Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
    }

    public static String getVersion() {
        return Server.class.getPackage().getImplementationVersion();
    }
}
