package es.thinkingmachin.linksight.imatch.server;

import es.thinkingmachin.linksight.imatch.matcher.dataset.ReferenceDataset;
import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.eval.Evaluator;
import es.thinkingmachin.linksight.imatch.matcher.matchers.DatasetMatcher;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeAddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference;

import java.util.List;

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
    }
}
